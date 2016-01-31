# -*- coding: utf-8 -*-
#
# Copyright (c) 2014-2016 Rodolphe Quiédeville <rodolphe@quiedeville.org>
# Copyright (c) 2014-2016 Agroof <http://www.agroof.net/>
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
from sigafo.osmboundary.models import Departement
from sigafo.ressources.models import Url
from sigafo.referentiel import models as refs
from sigafo.projet.models import Projet
from sigafo.utils.models import GeoHStoreManager
from random import random
import reversion
from django_pgjson.fields import JsonField
import json

# Site

class Site(models.Model):
    """Un site designe un lieu commun
    """
    name = models.CharField(max_length=300)
    address = models.TextField(blank=True)
    owner = models.ForeignKey(Contact, related_name='owner', blank=True, null=True)
    exploitant = models.ForeignKey(Contact, related_name='exploitant', blank=True, null=True)
    urls = models.ManyToManyField(Url, blank=True)
    comment = models.TextField(blank=True)

    #
    properties = JsonField(blank=True, null=True)

    # public info to display set on the map
    map_public_info = JsonField(blank=True, null=True)

    # updated by trigger
    nb_parcel = models.IntegerField(default=0)
    # updated by trigger
    nb_block = models.IntegerField(default=0)

    # Needed for some map, may be null
    projets = models.ManyToManyField(Projet, blank=True)
    
    center = models.PointField(blank=True, null=True)
    objects = models.GeoManager()

    def __unicode__(self):
        """
        The unicode method
        """
        return "%s" % (self.name)

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
        return Parcel.objects.filter(site=self)

    def get_blocks(self):
        return Block.objects.filter(parcel__site=self)

    @property
    def approx_center(self):
        """
        Here return real center for now

        Return : Point
        """
        if self.center is None:
            return None
        else:
            randx = 0
            randy = 0
            return Point(x=self.center.x + randx,
                         y=self.center.y + randy)


    @property
    def center_lat(self):
        if self.center:
            return self.center.y
        else:
            return 0

    @property
    def center_lon(self):
        if self.center:
            return self.center.x
        else:
            return 0


# Emplacements
class Parcel(models.Model):
    """The client as consummer
    """
    site = models.ForeignKey(Site,
                             on_delete=models.PROTECT)
    name = models.CharField(max_length=50)

    # who owned the parcel
    owner = models.ForeignKey(Contact,
                              related_name='powner',
                              blank=True,
                              null=True)

    # who works on the parcel
    exploitant = models.ForeignKey(Contact,
                                   related_name='pexploit',
                                   blank=True, null=True)

    # in ha
    surface = models.FloatField(blank=True, null=True)

    # 
    systemprod = models.ForeignKey(refs.SystemProd,
                                   blank=True,
                                   null=True)

    # in ha
    altitude = models.FloatField(blank=True, null=True)

    # in ha
    experimental = models.BooleanField(default=False)

    # Coordonnées GPS
    center = models.PointField(blank=True, null=True)
    polygon = models.PolygonField(blank=True, null=True)

    urls = models.ManyToManyField(Url, blank=True)

    # updated by trigger
    nb_block = models.IntegerField(default=0)
    # updated by triggers
    variables = hstore.DictionaryField(db_index=True,
                                       blank=True,
                                       null=True)

    # who create the map
    creator = models.ForeignKey(User)
    
    comment = models.TextField(blank=True)
    objects = GeoHStoreManager()


    def __unicode__(self):
        """
        The unicode method
        """
        return "%s - %s" % (self.site.name, self.name)

    @property
    def departement(self):
        """The title
        """
        return Departement.objects.filter(polygon__contains=self.center)


    @property
    def title(self):
        """The title
        """
        return "%s" % (self.name)

    @property
    def anonymous_title(self):
        """An anonymous title
        """
        return u"parcel_{}".format(self.id)


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

    def get_absolute_url(self):
        """Absolute url
        """
        return reverse('parcel_detail', args=[self.id])

    def get_blocks(self):
        return Block.objects.filter(parcel=self).only('name')

    @property
    def center_lat(self):
        if self.center:
            return self.center.y

    @property
    def center_lon(self):
        if self.center:
            return self.center.x


# Block, sous-ensemble de la parcelle
class Block(models.Model):
    """
    Un block est un emplacement geographique avec une activité
    """
    parcel = models.ForeignKey(Parcel,
                               on_delete=models.PROTECT)
    
    name = models.CharField(max_length=300)
    
    surface = models.FloatField(blank=True, null=True)

    center = models.PointField(blank=True, null=True)

    date_debut = models.DateField(blank=True, null=True)
    date_fin = models.DateField(blank=True, null=True)

    # usage
    # referentiel
    usage = models.CharField(max_length=300, blank=True) 

    projets = models.ManyToManyField(Projet, blank=True)

    urls = models.ManyToManyField(Url, blank=True)

    comment = models.TextField(blank=True)
    variables = hstore.DictionaryField(db_index=True, blank=True, null=True)
    import_initial = hstore.DictionaryField(db_index=True, blank=True, null=True)

    #
    topography = models.ForeignKey(refs.Topography, blank=True, null=True)
    classph    = models.ForeignKey(refs.ClassePH, blank=True, null=True)
    classprof  = models.ForeignKey(refs.ClasseProfondeur, blank=True, null=True)
    classhumid = models.ForeignKey(refs.ClasseHumidity, blank=True, null=True)

    # Production vegetales annuelles
    prod_veg_an = models.TextField()

    # Production vegetales perennes
    prod_veg_per = models.TextField()

    # Production animale
    prod_animal = models.TextField()

    # Façon culturale
    tillage = models.ManyToManyField(refs.Tillage,
                                     blank=True)

    # Fertilisation
    fertilisation = models.ManyToManyField(refs.Fertilisation,
                                           blank=True)

    # Traitement phytosanitaire
    traitphyto = models.ManyToManyField(refs.TraitPhyto,
                                        blank=True)

    # Mode de conduite
    conduite = models.ManyToManyField(refs.ModeConduite,
                                      blank=True)


    #
    properties = JsonField(blank=True, null=True)

    # public info to display set on the map
    map_public_info = JsonField(blank=True, null=True)

    # nombre d'amenagement (mise à jour par Trigger)
    nb_amg = models.IntegerField(default=0)

    objects = GeoHStoreManager()


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
        return "%s" % (self.name)


    def get_absolute_url(self):
        """Absolute url
        """
        return reverse('block_detail', args=[self.id])

    def get_observations(self):
        return Observation.objects.filter(block=self).order_by('-date_observation')

    # def save(self, *args, **kwargs):
    #     #check if the row with this hash already exists.
    #     with transaction.atomic(), reversion.create_revision():
    #         super(Block, self).save(*args, **kwargs)


class Observation(models.Model):
    """Observation
    """
    author = models.ForeignKey(User)
    block = models.ForeignKey(Block)
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

        We display the related block
        """
        return reverse('block_detail', args=[self.block.id])



#reversion.register(Parcel)
#reversion.register(Block)

