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
from django.db import models
from sigafo.contact.models import Contact, Organisme
from django.core.urlresolvers import reverse
from django_hstore import hstore
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Thematique(models.Model):
    """Thematique projet
    """
    name = models.CharField(max_length=300)
    comment = models.TextField(blank=True)

    def __unicode__(self):
        """The unicode method
        """
        return "%s" % (self.name)


class Projet(models.Model):
    """Projet
    """
    name = models.CharField(max_length=50)

    # est-ce un projet de recherche
    taxon = models.IntegerField(choices=((1,'Research'),
                                         (2, 'Territory'),
                                         (3, 'Formation')))

    annee_debut = models.IntegerField(blank=True, null=True)
    annee_fin = models.IntegerField(blank=True, null=True)

    referent_interne = models.ForeignKey(User,
                                         blank=True,
                                         null=True)

    objectifs = models.TextField(blank=True)
    description = models.TextField(blank=True)

    code = models.CharField(max_length=50, db_index=True, unique=True)

    # personnes incluses dans le projet
    coordinators = models.ManyToManyField(Contact,
                                          related_name='coordinator',
                                          blank=True)

    # personnes incluses dans le projet
    users = models.ManyToManyField(User, related_name='user', blank=True)

    # personnes incluses dans le projet
    partenaires = models.ManyToManyField(Organisme, related_name='partenaire', blank=True)

    # financeurs du projets
    financeurs = models.ManyToManyField(Organisme, related_name='financeur', blank=True)

    # thematiques projet
    thematiques = models.ManyToManyField(Thematique, blank=True)


    data = hstore.DictionaryField(db_index=True, blank=True)

    url = models.URLField(blank=True, null=True)

    objects = hstore.HStoreManager()


    def __unicode__(self):
        """The unicode method
        """
        return "%s" % (self.name)

    def get_absolute_url(self):
        """Absolute url
        """
        return reverse('projet_detail', args=[self.id])

    def taxon_str(self):
        return ('Research', 'Territory', 'Formation')[self.taxon]


class Comment(models.Model):
    """Commentaire sur le projet
    """
    projet = models.ForeignKey(Projet)
    creation = models.DateField(auto_now=True)
    author = models.ForeignKey(User, blank=True, null=True)
    private = models.BooleanField(default=True)
    comment = models.TextField(blank=True)

    @property
    def abstract(self):
        if len(self.comment) > 60:
            return "%s..." % (self.comment[:60])
        else:
            return "%s" % (self.comment)

    def __unicode__(self):
        """The unicode method
        """
        if len(self.comment) > 30:
            return "%s..." % (self.comment[:30])
        else:
            return "%s" % (self.comment)


def projet_add_all_staff(sender, instance, created, **kwargs):
    """All staff members in project
    """
    if created:
        for user in User.objects.filter(is_staff=True):
            instance.users.add(user)

post_save.connect(projet_add_all_staff, sender=Projet)
