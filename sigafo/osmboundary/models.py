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
from django.db import transaction
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django_hstore import hstore
from django.core.urlresolvers import reverse
from django.contrib.gis.geos.point import Point
from sigafo.contact.models import Contact
from sigafo.ressources.models import Url
from sigafo.referentiel import models as refs
from sigafo.projet.models import Projet
from sigafo.utils.models import GeoHStoreManager
from random import random
import reversion




# Block, sous-ensemble de la parcelle
class Block(models.Model):
    """
    Un block est un emplacement geographique avec une activité
    """
    name = models.CharField(max_length=50)

    center = models.PointField(blank=True, null=True)
    polygon = models.PolygonField(blank=True, null=True)


    def __unicode__(self):
        """
        The unicode method
        """
        return "%s" % (self.name)


    def get_absolute_url(self):
        """Absolute url
        """
        return reverse('block_detail', args=[self.id])
