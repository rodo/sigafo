#
# Sigafo parc views
#
#
from django.views.generic import ListView
from django.views.generic import CreateView, UpdateView
from djgeojson.views import GeoJSONLayerView
from sigafo.agrof.models import Amenagement
from sigafo.parc.models import Parcel, Block, Site
from sigafo.projet.models import Projet
from sigafo.utils.view_mixins import DetailProtected, ListProtected, ProtectedMixin
from sigafo.parc import forms
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from django.views.generic.base import TemplateView
from rest_framework import generics
from sigafo.parc.serializers import ParcelSerializer
from sigafo.utils.view_mixins import APICacheMixin, APIPCacheMixin


class ParcelNew(ProtectedMixin, CreateView):
    model = Parcel
    form_class = forms.ParcelForm
    template_name = 'parc/parcel_new.html'

    def get_initial(self):
        initial = super(ParcelNew, self).get_initial()
        initial.update({'creator': self.request.user.id})
        return initial

    def form_valid(self, form):
        """Force the user to request.user"""
        self.object = form.save(commit=False)
        self.object.creator_id = self.request.user.id
        self.object.save()

        return super(MapNew, self).form_valid(form)


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
    paginate_by = 10


    def get_queryset(self):
        if not self.request.user.is_staff:
            blocks = Block.objects.filter(projets__users__in=[self.request.user.id]).only('name').distinct()
        else:
            blocks = Block.objects.all().only('name')
        return blocks


class BlockDetail(DetailProtected):
    model = Block

    def get_context_data(self, **kwargs):
        context = super(BlockDetail, self).get_context_data(**kwargs)
        context['amgs'] = Amenagement.objects.filter(block=self.object)

        return context


class BlockEdit(ProtectedMixin, UpdateView):
    model = Block
    form_class = forms.BlockForm
    template_name = 'parc/block_form.html'


class HomepageView(TemplateView):
    template_name = "newhome.html"
