#
# Sigafo map views
#
#
import json
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, CreateView, UpdateView
from djgeojson.views import GeoJSONLayerView
from djgeojson.serializers import Serializer as GeoJSONSerializer

from sigafo.parc.models import Parcel, Block
from sigafo.map.models import Map, MapProperty
from sigafo.utils.view_mixins import ProtectedMixin
from sigafo.map import forms
from django import http
from django.http import HttpResponse
from django.views.generic.detail import BaseDetailView

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from serializers import MapSerializer


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


class MapDetail(GeoJSONLayerView):
    model = Map
    geometry_field = 'approx_center'
    properties = ['title']

    def get_queryset(self):
        qs = super(MapDetail, self).get_queryset()
        qsp = MapProperty.objects.filter(wmap_id=self.kwargs['pk']).values_list('prop')
        self.properties = [str(prop[0]) for prop in qsp]
        sql = """WITH projets AS (
        SELECT projet_id FROM map_map_projets
        WHERE map_id = {0}
        )
        SELECT DISTINCT(parcel_id) as id FROM parc_block_projets, parc_block
        WHERE parc_block_projets.block_id= parc_block.id
        AND projet_id IN (SELECT projet_id FROM projets);
        """.format(self.kwargs['pk'])
        ids = [p.id for p in Parcel.objects.raw(sql)]
        features = Parcel.objects.filter(pk__in=ids)
        print self.properties
        return features

    # def get_context_data(self, **kwargs):
    #     context = super(MapDetail, self).get_context_data(**kwargs)
    #     qsp = MapProperty.objects.filter(wmap_id=self.kwargs['pk']).values_list('prop')
    #     context['properties'] = [str(prop[0]) for prop in qsp]

    #     return context


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
