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


class Essence(models.Model):
    """Essence d'arbre
    """
    name = models.CharField(max_length=300)
    comment = models.TextField(blank=True)

    def __unicode__(self):
        """
        The unicode method
        """
        return "%s" % (self.name)


class Amenagement(models.Model):
    """
    """
    blocks = models.ManyToManyField(Block)

    annee_debut = models.IntegerField(blank=True, null=True)
    annee_fin = models.IntegerField(blank=True, null=True)

    localisation = models.IntegerField(choices=((1, 'intraparcellaire'),
                                                 (2, 'périphérique')))

    #nature= models.ManyToManyField(Essence, blank=True)

    proportion_bloc = models.IntegerField(blank=True, null=True)
    
    name = models.CharField(max_length=300)
    essences = models.ManyToManyField(Essence, blank=True)

    # distance entre les arbres sur la ligne
    online_distance = models.FloatField(blank=True, null=True)

    # distance entre les lignes
    line_spacing = models.FloatField(blank=True, null=True)

    # Commentaires divers
    comment = models.TextField(blank=True)

    def __unicode__(self):
        """
        The unicode method
        """
        return "%s" % (self.name)


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
