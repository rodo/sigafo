#
# App : projet
#
from django.shortcuts import (get_object_or_404, redirect)
from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from sigafo.parc.models import Parcel, Block, Site
from sigafo.projet.models import Projet
from sigafo.utils.view_mixins import ProtectedMixin


class ProjetListView(ListView):
    model = Projet

    def get_queryset(self):
        return self.model.objects.filter(users__in=[self.request.user.pk])


class ProjetDetailView(ProtectedMixin, DetailView):
    model = Projet

    def get(self, *args, **kwargs):
        # Security to edit only own resume
        self.object = self.get_object()
        ids = [pki[0] for pki in self.object.users.values_list('pk')]
        if not self.request.user.id in ids:
            return redirect(reverse('projet_list'))
        return super(ProjetDetailView, self).get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProjetDetailView, self).get_context_data(**kwargs)
        context['blocks'] = Block.objects.filter(projets__in=[self.object.pk]).only('name')
        return context
