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
# App : agrof
#
from django.db import models, transaction
from django.contrib.auth.models import User
from sigafo.parc.models import Block
from sigafo.referentiel import models as refs
from django_pgjson.fields import JsonField
import json


# Aménagement
class Amenagement(models.Model):
    """
    Un aménagement est dans un block
    """
    block = models.ForeignKey(Block)
    
    name = models.CharField(max_length=300)

    date_debut = models.DateField(blank=True, null=True)
    date_fin = models.DateField(blank=True, null=True)

    localisation = models.IntegerField(blank=True, null=True,
                                       choices=((0, 'intra'),
                                                (1, 'periph')))

    nature = models.ForeignKey(refs.AmNature, blank=True, null=True)

    quality = models.IntegerField(blank=True, null=True,
                                  choices=((0, 'faible'),
                                           (1, 'moyenne'),
                                           (2, 'bonne')))

    proportion = models.IntegerField(blank=True, null=True)

    objectifs = models.ManyToManyField(refs.AmObjectifInit, blank = True)

    essences = models.ManyToManyField(refs.AmEssence, blank = True)

    conduites = models.ManyToManyField(refs.AmConduite, blank = True)    

    # année de plantation
    annee_plan = models.IntegerField(blank=True, null=True)

    # largeur de bande
    larg_band = models.IntegerField(blank=True, null=True)

    # lineaire de haie
    lin_haie = models.IntegerField(blank=True, null=True)

    # densité
    density = models.IntegerField(blank=True, null=True)

    # distance sur la ligne
    dist_on_line = models.IntegerField(blank=True, null=True)

    # distance entre les lignes
    dist_inter_line = models.IntegerField(blank=True, null=True)

    # distance entre les lignes de taillis
    dist_inter_taillis = models.IntegerField(blank=True, null=True)

    # Largeur tournières
    larg_tourn = models.IntegerField(blank=True, null=True)

    # Protections
    protections = models.ManyToManyField(refs.AmProtection, blank=True)    

    # Paillage
    protections = models.ManyToManyField(refs.AmPaillage, blank=True)    

    # commentaires sur les arbres
    comm_arbre = models.TextField(blank=True, null=True)    

    # Nature de la bande enherbée
    nature_be = models.ForeignKey(refs.AmNaturebe, blank=True, null=True)    

    # Gestion de la bande enherbée
    gestion_be = models.ManyToManyField(refs.AmGestionbe, blank=True)    

    # commentaires sur la bande enherbée
    comm_be = models.TextField(blank=True, null=True)    

    #
    properties = JsonField(blank=True, null=True)

    #
    map_public_info = JsonField(blank=True, null=True)


class Indicator(models.Model):
    """
    Indicateur utilisé dans un protocole de suivi
    """
    author = models.ForeignKey(User)
    name = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    comment = models.TextField(blank=True)
    note = models.TextField(blank=True)

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


class Measure(models.Model):
    """
    Relevé de mesure
    """
    author = models.ForeignKey(User)
    indicator = models.ForeignKey(Indicator)
    block = models.ForeignKey(Block)
    value = models.FloatField()
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
