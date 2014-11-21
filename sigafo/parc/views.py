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
from rest_framework import generics
from sigafo.parc.serializers import ParcelSerializer
from sigafo.utils.view_mixins import APICacheMixin, APIPCacheMixin


class ParcelJSONList(APIPCacheMixin, generics.ListAPIView):
    #queryset = Parcel.objects.all()
    serializer_class = ParcelSerializer
    paginate_by = 3

    def get_queryset(self):
        if not self.request.user.is_staff:
            parcels = Parcel.objects.filter(block__projets__users__in=[self.request.user.id]).only('name').distinct()
        else:
            parcels = Parcel.objects.all().only('name')
        return parcels


class SiteList(ProtectedMixin, ListView):
    model = Site

    def get_queryset(self):
        if not self.request.user.is_staff:
            sites = Site.objects.filter(parcel__block__projets__users__in=[self.request.user.id]).only('name').distinct()
        else:
            sites = Site.objects.all().only('name')
        return sites


class ParcelList(ProtectedMixin, ListView):
    def get_queryset(self):
        if not self.request.user.is_staff:
            parcels = Parcel.objects.filter(block__projets__users__in=[self.request.user.id]).only('name').distinct()
        else:
            parcels = Parcel.objects.all().only('name')
        return parcels


class BlockList(ProtectedMixin, ListView):
    """List all Blocks
    we filter by project for non staff members
    """
    def get_queryset(self):
        if not self.request.user.is_staff:
            blocks = Block.objects.filter(projets__users__in=[self.request.user.id]).only('name').distinct()
        else:
            blocks = Block.objects.all().only('name')
        return blocks


class HomepageView(TemplateView):
    template_name = "newhome.html"


class BlockEdit(ProtectedMixin, UpdateView):
    model = Block
    form_class = forms.BlockForm
    template_name = 'parc/block_form.html'
