#
# Sigafo main URLS
#
#
from django.conf.urls import patterns, include, url
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.contrib import admin
from sigafo.contact.models import Contact
from sigafo.parc.models import Champ, Parcel, Site
from sigafo.parc.views import HomepageView
from sigafo.projet.models import Projet
from djgeojson.views import GeoJSONLayerView

from sigafo.projet import views

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', HomepageView.as_view()),
                       url(r'^search/', include('haystack.urls')),
                       url(r'^site/(?P<pk>\d+)$', DetailView.as_view(model=Site), name='site_detail'),
                       url(r'^contact/(?P<pk>\d+)$', DetailView.as_view(model=Contact), name='contact_detail'),
                       url(r'^champ/(?P<pk>\d+)$', DetailView.as_view(model=Champ), name='champ_detail'),
                       url(r'^parcel/list$', ListView.as_view(model=Parcel), name='parcel_list'),
                       url(r'^parcel/(?P<pk>\d+)$', DetailView.as_view(model=Parcel), name='parcel_detail'),
                       url(r'^parcel/new$', ListView.as_view(model=Parcel), name='parcel_new'),
                       url(r'^parcel/geojson$', GeoJSONLayerView.as_view(model=Parcel,
                                                                         geometry_field='approx_center'), name='parcel_geojson'),
                       url(r'^projet/list$', views.ProjetListView.as_view(), name='projet_list'),
                       url(r'^projet/(?P<pk>\d+)$', views.ProjetDetailView.as_view(), name='projet_detail'),
                       url(r'^projet/new$', ListView.as_view(model=Projet), name='projet_new'),
                       url(r'^sites/$', ListView.as_view(model=Site), name='site_list'),
)
