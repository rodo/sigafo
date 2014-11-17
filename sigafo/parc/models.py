# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 Rodolphe Quiédeville <rodolphe@quiedeville.org>
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
from sigafo.contact.models import Contact
from sigafo.projet.models import Projet
from django.contrib.gis.geos.point import Point
from random import random
import reversion

class MonManager(models.GeoManager, hstore.HStoreManager):
    pass
    
# Site

class Site(models.Model):
    """
    Un site designe un lieu commune
    """
    name = models.CharField(max_length=300)
    address = models.TextField(blank=True)
    owner = models.ForeignKey(Contact, related_name='owner', blank=True, null=True)
    exploitant = models.ForeignKey(Contact, related_name='exploitant', blank=True, null=True)
    comment = models.TextField(blank=True)

    def __unicode__(self):
        """
        The unicode method
        """
        return u"{}".format(self.name)

    def __str__(self):
        """
        The string method
        """
        return "{}".format(self.name)

    def get_absolute_url(self):
        """
        Absolute url
        """
        return reverse('site_detail', args=[self.id])

    def get_parcels(self):
        return Parcel.objects.filter(champ__site=self)

    def get_champs(self):
        return Champ.objects.filter(site=self)


# Emplacements
class Champ(models.Model):
    """The client as consummer
    """
    site = models.ForeignKey(Site)
    name = models.CharField(max_length=50)
    comment = models.TextField(blank=True)

    def __unicode__(self):
        """
        The unicode method
        """
        return u"{}".format(self.name)

    def __str__(self):
        """
        The string method
        """
        return "{}".format(self.name)

    def get_absolute_url(self):
        """Absolute url
        """
        return reverse('champ_detail', args=[self.id])

    def get_parcels(self):
        return Parcel.objects.filter(champ=self).only('name')


# Parcelles
class Parcel(models.Model):
    """
    Une parcelle est un emplacement geographique avec une activité
    """
    champ = models.ForeignKey(Champ)
    name = models.CharField(max_length=50)
    surface = models.FloatField(blank=True, null=True)

    center = models.PointField(blank=True, null=True)
    date_debut = models.DateField(blank=True, null=True)
    date_fin = models.DateField(blank=True, null=True)
    usage = models.CharField(max_length=300, blank=True) # referentiel
    projet = models.ManyToManyField(Projet, blank=True)
    comment = models.TextField(blank=True)
    variables = hstore.DictionaryField(db_index=True)
    import_initial = hstore.DictionaryField(db_index=True)
    objects = MonManager()


    @property
    def approx_center(self):
        """
        Fake coordinate based on real coordinate

        Return : Point        
        """
        if self.center is None:
            return None
        else:
            randx = (0.5 - random())/21
            randy = (0.5 - random())/21
            return Point(x=self.center.x + randx,
                         y=self.center.y + randy)

    def __unicode__(self):
        """
        The unicode method
        """
        return u"{}".format(self.name)

    def __str__(self):
        """
        The string method
        """
        return "{}".format(self.name)

    def get_absolute_url(self):
        """Absolute url
        """
        return reverse('parcel_detail', args=[self.id])

    def get_observations(self):
        return Observation.objects.filter(parcel=self).order_by('-date_observation')

    def save(self, *args, **kwargs):
        #check if the row with this hash already exists.
        with transaction.atomic(), reversion.create_revision():
            super(Parcel, self).save(*args, **kwargs)


class Observation(models.Model):
    """Observation
    """
    author = models.ForeignKey(User)
    parcel = models.ForeignKey(Parcel)
    date_observation = models.DateField(auto_now=True)
    observation = models.TextField(blank=True)
    comment = models.TextField(blank=True)
    private = models.BooleanField(default=True)

    def __unicode__(self):
        """
        The unicode method
        """
        return "observation {}".format(self.id)

    def __str__(self):
        """
        The string method
        """
        return "observation {}".format(self.id)

    def get_absolute_url(self):
        """Absolute url

        We display the related parcel
        """
        return reverse('parcel_detail', args=[self.parcel.id])

reversion.register(Parcel)
