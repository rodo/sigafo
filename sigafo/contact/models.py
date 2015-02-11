# -*- coding: utf-8 -*-
#
# Copyright (c) 2014,2015 Rodolphe Quiédeville <rodolphe@quiedeville.org>
# Copyright (c) 2014,2015 Agroof <http://www.agroof.net/>
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
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from json_field import JSONField
import json


class Activite(models.Model):
    """
    Activite des contacts
    agriculteurs, chercheurs
    """
    name = models.CharField(max_length=50)
    comment = models.TextField(blank=True)

    def __unicode__(self):
        """The unicode method
        """
        return u"{}".format(self.name)

    def __str__(self):
        """The string method
        """
        return "{}".format(self.name)


class Contact(models.Model):
    """
    Contact générique
    """
    SEX = (
        (1, 'Man'),
        (2, 'Woman'),
        (3, 'Not specified'))

    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    address = models.TextField(blank=True, null=True)
    phonenumber = models.CharField(max_length=50, blank=True)
    sex = models.PositiveSmallIntegerField(blank=True,
                                           null=True,
                                           choices=SEX)
    birthdate = models.DateField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    activite = models.ForeignKey(Activite, blank=True, null=True)
    comment = models.TextField(blank=True)

    user = models.ForeignKey(User, blank=True, null=True)

    properties = JSONField(blank=True, null=True)

    # public info to display set on the map
    map_public_info = JSONField(blank=True, null=True)


    def __unicode__(self):
        """The unicode method
        """
        return "%s %s" % (self.lastname, self.firstname)

    def get_absolute_url(self):
        """
        Absolute url
        """
        return reverse('contact_detail', args=[self.id])

    def name(self):
        """Name
        """
        return "%s %s" % (self.lastname, self.firstname)


class Organisme(models.Model):
    """Organisme
    """
    name = models.CharField(max_length=150)
    address = models.TextField(blank=True, null=True)
    phonenumber = models.CharField(max_length=50, blank=True)
    url = models.URLField(blank=True, null=True)
    contacts = models.ManyToManyField(Contact, blank=True)

    comment = models.TextField(blank=True)

    def __unicode__(self):
        """The unicode method
        """
        return "%s" % (self.name)

    def get_absolute_url(self):
        """Absolute url
        """
        return reverse('contact_detail', args=[self.id])
