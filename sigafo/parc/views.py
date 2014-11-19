#
# Sigafo parc views
#
#
from django.views.generic import ListView
from django.views.generic import CreateView, UpdateView
from djgeojson.views import GeoJSONLayerView
from sigafo.parc.models import Parcel, Block, Site
from sigafo.projet.models import Projet
from sigafo.utils.view_mixins import ProtectedMixin
from sigafo.parc import forms
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from django.views.generic.base import TemplateView


class SiteList(ProtectedMixin, ListView):
    model = Site

    def get_queryset(self):
        sites = Site.objects.filter(parcel__block__projets__users__in=[self.request.user.id]).only('name').distinct()
        return sites


class ParcelList(ProtectedMixin, ListView):
    def get_queryset(self):
        parcels = Parcel.objects.filter(block__projets__users__in=[self.request.user.id]).only('name').distinct()
        return parcels


class BlockList(ProtectedMixin, ListView):
    def get_queryset(self):
        blocks = Block.objects.filter(projets__users__in=[self.request.user.id]).only('name').distinct()
        return blocks


class HomepageView(TemplateView):
    template_name = "newhome.html"


class BlockEdit(ProtectedMixin, UpdateView):
    model = Block
    form_class = forms.BlockForm
    template_name = 'parc/block_form.html'
