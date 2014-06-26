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
from django.contrib.gis.db import models
from django.core.urlresolvers import reverse
from sigafo.contact.models import Contact
from sigafo.projet.models import Projet
import reversion


# Site
class Site(models.Model):
    """
    Un site designe un lieu commune
    """
    name = models.CharField(max_length=300)
    owner = models.ForeignKey(Contact, related_name='owner')
    exploitant = models.ForeignKey(Contact, related_name='exploitant')

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

# Emplacements
class Champ(models.Model):
    """The client as consummer
    """
    site = models.ForeignKey(Site)
    name = models.CharField(max_length=300)

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
    projet = models.ManyToManyField(Projet)

    objects = models.GeoManager()

    @property
    def approx_center(self):
        return self.center

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
        return reverse('parcel_detail', args=[self.id])

    def save(self, *args, **kwargs):
        #check if the row with this hash already exists.
        with transaction.atomic(), reversion.create_revision():
            super(Parcel, self).save(*args, **kwargs)


reversion.register(Parcel)
