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

class MapManager(models.GeoManager, hstore.HStoreManager):
    pass


class Map(models.Model):
    """Map
    """
    title = models.CharField(max_length=50)
    creator = models.ForeignKey(User)
    projets = models.ManyToManyField(Projet, blank=True)
    # properties available/displayed on map
    properties = hstore.DictionaryField(db_index=True, blank=True, null=True)

    center = models.PointField(blank=True, null=True)

    published = models.BooleanField(default=False)
    # public_map : the geojson is open to everybody    
    public_map = models.BooleanField(default=False)

    objects = MapManager()
    
    def __unicode__(self):
        """
        The unicode method
        """
        return u"{}".format(self.title)

    def __str__(self):
        """
        The string method
        """
        return "{}".format(self.title)

    def get_absolute_url(self):
        """Absolute url
        """
        return reverse('map_detail', args=[self.id])

