#
# Sigafo map views
#
#
from django.core.urlresolvers import reverse
from django.views.generic import CreateView
from djgeojson.views import GeoJSONLayerView
from sigafo.parc.models import Parcel
from sigafo.map.models import Map
from sigafo.utils.view_mixins import ProtectedMixin
from sigafo.map import forms


class MapDetail(ProtectedMixin, GeoJSONLayerView):
    model = Parcel
    properties=['title']
    geometry_field='approx_center'


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
