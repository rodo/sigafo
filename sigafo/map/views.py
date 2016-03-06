# -*- coding: utf-8 -*-
#
# Copyright (c) 2014,2015 Rodolphe Quiédeville <rodolphe@quiedeville.org>
# Copyright (c) 2014,2015 Agroof <http://www.agroof.net/>
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
# Sigafo map views
#
#
from django.db import connection
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, UpdateView
from django.contrib.gis.shortcuts import render_to_kml
from django.http import HttpResponse
from djgeojson.views import GeoJSONLayerView
from sigafo.parc.models import Parcel, Block
from sigafo.parc.models import Site
from sigafo.map.models import Map
from sigafo.utils.view_mixins import ProtectedMixin
from sigafo.map import forms
from rest_framework.renderers import JSONRenderer
from serializers import MapSerializer
import json
from djgeojson.serializers import Serializer as GeoJSONSerializer


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)



def parcel_sql(map_id, parcel_id):
    cursor = connection.cursor()

    table = "v_map_%s_parcel" % map_id
    qry = "SELECT map_public_info FROM {0} WHERE id = %s".format(table)
    cursor.execute(qry, [parcel_id])
    row = cursor.fetchone()
    parcel = row[0]
    return parcel


class MapDetail(GeoJSONLayerView):
    model = Map
    geometry_field = 'approx_center'
    properties = ['title']

    def dispatch(self, *args, **kwargs):
        response = super(GeoJSONLayerView, self).dispatch(*args, **kwargs)
        data = json.loads(response.content)
        # lookup for additionnal properties
        for i in range(0, len(data['features'])):
            prop = data['features'][i]['properties']
            nprop = parcel_sql(self.kwargs['pk'],
                               data['features'][i]['id'])

            data['features'][i]['properties'] = nprop

        # set new data
        response.content = json.dumps(data)
        return response

    def get_queryset(self):
        super(MapDetail, self).get_queryset()
        qsp = Map.objects.get(pk=self.kwargs['pk'])
        self.properties = [prop.key for prop in qsp.properties.all()]

        if qsp.model == 'Block':
            sql = """WITH projets AS (
            SELECT projet_id FROM map_map_projets
            WHERE map_id = {0}
            )
            SELECT parc_block.id FROM parc_block_projets, parc_block
            WHERE parc_block_projets.block_id= parc_block.id
            AND projet_id IN (SELECT projet_id FROM projets);
            """.format(self.kwargs['pk'])

            ids = [p.id for p in Block.objects.raw(sql)]
            features = Block.objects.filter(pk__in=ids)

        if qsp.model == 'Parcel':
            """
            Selection de toutes les parcelles dont au moins un bloc est dans le projet
            """
            sql = """
            WITH projets AS (
            SELECT projet_id FROM map_map_projets
            WHERE map_id = {0}
            )
            SELECT DISTINCT(parcel_id) as id FROM parc_block_projets, parc_block
            WHERE parc_block_projets.block_id= parc_block.id
            AND projet_id IN (SELECT projet_id FROM projets);
            """.format(self.kwargs['pk'])

            ids = [p.id for p in Parcel.objects.raw(sql)]
            features = Parcel.objects.filter(pk__in=ids)

        if qsp.model == 'Site':
            sql = """WITH projets AS (
            SELECT projet_id FROM map_map_projets
            WHERE map_id = {0}
            )
            SELECT DISTINCT(site_id) as id FROM parc_site_projets, parc_site
            WHERE parc_site_projets.site_id = parc_site.id
            AND projet_id IN (SELECT projet_id FROM projets);
            """.format(self.kwargs['pk'])

            ids = [p.id for p in Parcel.objects.raw(sql)]
            features = Site.objects.filter(pk__in=ids)

        return features


class MapNew(ProtectedMixin, CreateView):
    model = Map
    form_class = forms.MapForm
    template_name = 'map/map_new.html'

    def get_initial(self):
        initial = super(MapNew, self).get_initial()
        initial.update({'creator': self.request.user.id})
        return initial

    def form_valid(self, form):
        """Force the user to request.user"""
        self.object = form.save(commit=False)
        self.object.creator_id = self.request.user.id
        self.object.save()

        return super(MapNew, self).form_valid(form)


class MapEdit(ProtectedMixin, UpdateView):
    model = Map
    form_class = forms.MapForm
    template_name = 'map/map_new.html'


@csrf_exempt
def map_json(request, pk):
    """
    Retrieve, update or delete a code map.
    """
    try:
        map = Map.objects.get(pk=pk)
    except Map.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = MapSerializer(map)
        return JSONResponse(serializer.data)


@csrf_exempt
@cache_page(60 * 15)
def map_kml(request, pk):
    """Export datas in kml  format
    """
    qsp = MapProperty.objects.filter(wmap_id=pk)
    properties = [str(prop[0]) for prop in qsp.values_list('prop')]
    sql = """WITH projets AS (
    SELECT projet_id FROM map_map_projets
    WHERE map_id = {0}
    )
    SELECT DISTINCT(parcel_id) as id FROM parc_block_projets, parc_block
    WHERE parc_block_projets.block_id= parc_block.id
    AND projet_id IN (SELECT projet_id FROM projets);
    """.format(pk)
    ids = [p.id for p in Parcel.objects.raw(sql)]
    features = Parcel.objects.filter(pk__in=ids)

    return render_to_kml("map_parcel.kml", {'places': features})

@csrf_exempt
def map_jsonp(request, pk):
    """Export datas in jsonp
    """
    map = Map.objects.get(pk=pk)

    if map.model == 'Block':
        view = MapDetail(model=Block,kwargs={'pk': pk})

    if map.model == 'Parcel':
        view = MapDetail(model=Parcel,kwargs={'pk': pk})
        #view.object_list = [Parcel.objects.get(pk=pk)]

    if map.model == 'Site':
        view = MapDetail(model=Site,kwargs={'pk': pk})

    resp = view.render_to_response(context={})
    content = resp.content
    try:
        data = '%s(%s);' % (request.REQUEST['callback'], content)
    except:
        data = '%s(%s);' % (request.REQUEST['callback'], content.decode('utf-8'))

    return HttpResponse(data, "text/javascript")
