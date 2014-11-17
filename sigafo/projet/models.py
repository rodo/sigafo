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
from sigafo.contact.models import Contact
from django.core.urlresolvers import reverse
from django_hstore import hstore
from django.contrib.auth.models import User

    
class Projet(models.Model):
    """Projet
    """
    name = models.CharField(max_length=50)

    # est-ce un projet de recherche
    research = models.BooleanField(default=True)
    # est-ce un projet territoire
    territory = models.BooleanField(default=False)

    date_debut = models.DateField(blank=True, null=True)
    date_fin = models.DateField(blank=True, null=True)

    referent_interne = models.ForeignKey(Contact, blank=True, null=True)

    description = models.TextField(blank=True)
    comments = models.TextField(blank=True)

    # personnes incluses dans le projet
    users = models.ManyToManyField(User, blank=True)

    data = hstore.DictionaryField(db_index=True)
    objects = hstore.HStoreManager()


    def __unicode__(self):
        """The unicode method
        """
        return u"{}".format(self.name)

    def __str__(self):
        """The string method
        """
        return "{}".format(self.name)

    def get_absolute_url(self):
        """Absolute url
        """
        return reverse('projet_detail', args=[self.id])


