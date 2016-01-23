#
# Sigafo main URLS
#
#
from django.conf.urls import patterns, include, url
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.contrib import admin
from djgeojson.views import GeoJSONLayerView
from sigafo.contact.models import Contact
from sigafo.parc.models import Parcel, Block, Site
from sigafo.map.models import Map
from sigafo.parc.views import HomepageView
from sigafo.projet.models import Projet
from sigafo.utils.view_mixins import DetailProtected, ListProtected
from sigafo.projet import views
from sigafo.map import views as mapviews
from sigafo.parc import views as parcviews
from sigafo.contact import views as contactviews
from sigafo.referentiel import views as refviews

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', HomepageView.as_view()),
    url(r'^search/', include('haystack.urls')),
    
    url(r'^site/$',
        parcviews.SiteList.as_view(model=Site,
                                   paginate_by=10
                                   ),
        name='site_list'),
    
    url(r'^site/(?P<pk>\d+)$',
        DetailProtected.as_view(model=Site),
        name='site_detail'),
    
    url(r'^contact/$',
        contactviews.ContactList.as_view(model=Contact,
                                         paginate_by=10
                                         ),
        name='contact_list'),
    
    url(r'^contact/(?P<pk>\d+)$',
        DetailProtected.as_view(model=Contact),
        name='contact_detail'),

    #url(r'^contact/json/$',
    #contactviews.ContactJSONList.as_view(),
    #name='contact_json'),


    url(r'^map/$', ListProtected.as_view(model=Map,
                                         queryset=Map.objects.order_by("-pk").only('title'),
                                         ), name='map_list'),
    url(r'^map/new$', mapviews.MapNew.as_view(model=Map), name='map_new'),
    url(r'^map/(?P<pk>\d+)$', DetailProtected.as_view(model=Map), name='map_detail'),
    url(r'^map/(?P<pk>\d+)/edit$', mapviews.MapEdit.as_view(model=Map), name='map_edit'),
    url(r'^map/(?P<pk>\d+)/json$', mapviews.map_json, name='map_json'),
    url(r'^map/(?P<pk>\d+)/kml21$', mapviews.map_kml, name='map_kml21'),
    url(r'^map/(?P<pk>\d+)/geojson$', mapviews.MapDetail.as_view(), name='map_geojson'),
    url(r'^map/(?P<pk>\d+)/geojsonp$', mapviews.map_jsonp, name='map_geojsonp'),
    
    url(r'^parcel/(?P<pk>\d+)$', DetailProtected.as_view(model=Parcel), name='parcel_detail'),
    url(r'^parcel/new$', parcviews.ParcelNew.as_view(), name='parcel_new'),
    url(r'^parcel/$', parcviews.ParcelList.as_view(model=Parcel,
                                                   paginate_by=10), name='parcel_list'),
    url(r'^parcel/json/$', parcviews.ParcelJSONList.as_view(), name='parcel_json'),
    url(r'^parcel/geojson$', GeoJSONLayerView.as_view(model=Parcel,
                                                      properties=['title'],
                                                      geometry_field='approx_center'), name='parcel_geojson'),
    
    url(r'^block/$', parcviews.BlockList.as_view(model=Block), name='block_list'),
    url(r'^block/(?P<pk>\d+)$', DetailProtected.as_view(model=Block), name='block_detail'),
    url(r'^block/(?P<pk>\d+)/import$', DetailProtected.as_view(model=Block,
                                                               template_name="parc/block_import.html"), name='block_import'),
    url(r'^block/(?P<pk>\d+)/edit$', parcviews.BlockEdit.as_view(), name='block_edit'),
    url(r'^block/new$', ListProtected.as_view(model=Block), name='block_new'),
    url(r'^block/geojson$', GeoJSONLayerView.as_view(model=Block,
                                                     geometry_field='approx_center'), name='block_geojson'),
    
    url(r'^project/$', views.ProjetListView.as_view(), name='projet_list'),
    url(r'^project/(?P<pk>\d+)$', views.ProjetDetailView.as_view(), name='projet_detail'),
    url(r'^project/new$', ListProtected.as_view(model=Projet), name='projet_new'),
    url(r'^accounts/profile/$', 'sigafo.users.views.profile', name='profile'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    
    url(r'^referentiel/json/$', refviews.TopographyList.as_view(), name='referentiel_json'),
)
