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
from django.db import models
from django.core.urlresolvers import reverse


class Activite(models.Model):
    """
    Activite des contacts
    agriculteurs, chercheurs
    """
    name = models.CharField(max_length=50)
    comment = models.TextField(blank=True)


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
    address = models.CharField(max_length=150, blank=True)
    phonenumber = models.CharField(max_length=50, blank=True)
    sex = models.PositiveSmallIntegerField(blank=True, 
                                           null=True,
                                           choices=SEX)
    birthdate = models.DateField(blank=True, null=True)
    email = models.EmailField()
    activite = models.ForeignKey(Activite)
    comment = models.TextField(blank=True)

    def __unicode__(self):
        """
        The unicode method
        """
        return u"{} {}".format(self.lastname, self.firstname)

    def __str__(self):
        """
        The string method
        """
        return "{} {}".format(self.lastname, self.firstname)

    def get_absolute_url(self):
        """
        Absolute url
        """
        return reverse('contact_detail', args=[self.id])
