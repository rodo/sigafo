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
from sigafo.parc.models import Parcel


class Essence(models.Model):
    """
    Essence de bois
    """
    name = models.CharField(max_length=300)
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


class Peuplement(models.Model):
    """

    """
    parcel = models.ForeignKey(Parcel)
    name = models.CharField(max_length=300)
    essences = models.ManyToManyField(Essence)
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


class Indicator(models.Model):
    """
    Indicateur utilisé dans un protocole de suivi
    """
    author = models.ForeignKey(User)
    name = models.CharField(max_length=300)
    description = models.TextField(blank=True)
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

    note = models.TextField(blank=True)


class Measure(models.Model):
    """
    Relevé de mesure
    """
    author = models.ForeignKey(User)
    indicator = models.ForeignKey(Indicator)
    parcel = models.ForeignKey(Parcel)
    value = models.FloatField()
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
