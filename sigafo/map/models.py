# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 Rodolphe Quiédeville <rodolphe@quiedeville.org>
# Copyright (c) 2014 Agroof <http://www.agroof.net/>
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
from django.contrib.gis.db import models
from sigafo.projet.models import Projet
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django_hstore import hstore
from sigafo.utils.models import GeoHStoreManager
from django_pgjson.fields import JsonField
from sigafo.parc.models import Block
from sigafo.parc.models import Parcel
from sigafo.parc.models import Site


class ModelProperty(models.Model):
    """Model property
    """
    model = models.CharField(max_length=50)
    key = models.CharField(max_length=50)
    name = models.CharField(max_length=200)

    def __unicode__(self):
        """
        The unicode method
        """
        return "%s" % (self.name)


class Map(models.Model):
    """Map
    """
    # the title map
    title = models.CharField(max_length=50)
    # Projects which the map is belong to
    projets = models.ManyToManyField(Projet, blank=True)

    # which model the map is related to
    model = models.CharField(max_length=10,
                             choices=(('Parcel', 'Parcel'),
                                      ('Block', 'Block'),
                                      ('Site', 'Site')))

    # center of the map, automatically filled with database trigger
    center = models.PointField(blank=True, null=True)

    # lang of the map
    lang = models.CharField(max_length=10)

    # is the map published or not
    published = models.BooleanField(default=False)

    # public_map : the geojson is open to everybody
    public_map = models.BooleanField(default=False)

    # Projects which the map is belong to
    properties = models.ManyToManyField(ModelProperty, blank=True)

    # properties available/displayed on map
    static_properties = hstore.DictionaryField(db_index=True,
                                               blank=True,
                                               null=True)

    # who create the map
    creator = models.ForeignKey(User)

    objects = GeoHStoreManager()

    def __unicode__(self):
        """
        The unicode method
        """
        return "%s" % (self.title)

    def get_absolute_url(self):
        """Absolute url
        """
        return reverse('map_detail', args=[self.id])

    @property
    def center_lat(self):
        return self.center.y

    @property
    def center_lon(self):
        return self.center.x


class ParcelMap(models.Model):
    """
    Un parcel est un emplacement geographique avec une activité
    """
    map = models.ForeignKey(Map)
    parcel = models.ForeignKey(Parcel)

    map_public_info = JsonField(blank=True, null=True)


class SiteMap(models.Model):
    """
    Un site est un emplacement geographique avec une activité
    """
    map = models.ForeignKey(Map)
    site = models.ForeignKey(Site)

    map_public_info = JsonField(blank=True, null=True)


class BlockMap(models.Model):
    """
    Un block est un emplacement geographique avec une activité
    """
    map = models.ForeignKey(Map)
    block = models.ForeignKey(Block)

    map_public_info = JsonField(blank=True, null=True)
