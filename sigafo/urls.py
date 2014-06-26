from django.conf.urls import patterns, include, url
from django.views.generic import ListView

from django.views.generic.detail import DetailView
from django.contrib import admin
from sigafo.parc.models import Champ, Parcel, Site
from sigafo.parc.views import HomepageView
from djgeojson.views import GeoJSONLayerView

admin.autodiscover()



urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', HomepageView.as_view()),
                       url(r'^parcel/list$', ListView.as_view(model=Parcel), name='parcel_list'),
                       url(r'^parcel/(?P<pk>\d+)$', DetailView.as_view(model=Parcel), name='parcel_detail'),
                       url(r'^parcel/geojson$', GeoJSONLayerView.as_view(model=Parcel,
                                                                         geometry_field='approx_center'), name='parcel_geojson'),
                       url(r'^parcel/new$', ListView.as_view(model=Parcel), name='parcel_new'),
                       url(r'^sites/$', ListView.as_view(model=Site), name='site_list'),
)
