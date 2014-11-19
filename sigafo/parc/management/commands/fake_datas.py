#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013,2014 Rodolphe Quiédeville <rodolphe@quiedeville.org>
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

import sys
import os
import time
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from sigafo.ressources.models import Url
from sigafo.projet.models import Projet
from sigafo.referentiel.models import SystemProd
from sigafo.parc.models import Parcel, Block, Site
from sigafo.agrof.models import Essence, Amenagement
from sigafo.contact.models import Contact, Activite
from django.contrib.gis.geos.point import Point
from optparse import make_option
from faker import Faker
from django.db import connection
from random import randrange, random


class Command(BaseCommand):
    help = 'Import datas'
    option_list = BaseCommand.option_list + (
        make_option("-n",
                    "--nbvalues",
                    dest="nbvalues",
                    type="int",
                    help="number of values to input",
                    default=10),
        )

    def handle(self, *args, **options):
        """
        Make
        """
        nbvalues = options['nbvalues']
        self.insert(nbvalues)


    def insert(self, nbvalues):
        """
        Save values in DB
        """
        f = Faker()

        #peuplement = Peuplement.objects.create(name=f.name())
        #peuplement.essences.add(Essence.objects.get(pk=1))

        projet = Projet.objects.create(name=f.company())
        projet.users.add(User.objects.get(pk=1))
        projet.save()
        
        Contact.objects.create(firstname=f.first_name(),
                               lastname=f.last_name(),
                               activite=Activite.objects.all().last())

        syp = SystemProd.objects.all().last()

        for i in range(nbvalues):
            site = Site.objects.create(name=f.word(),
                                       owner=Contact.objects.all().last(),
                                       exploitant=Contact.objects.all().first(),)

            for p in range(randrange(2)):

                url = Url.objects.create(title=f.word(), url=f.url())

                center = Point(x=float(5 - randrange(8) + random()),
                               y=float(50 - randrange(8) + random()))

                parcel = Parcel.objects.create(name=f.word(),
                                               center=center,
                                               site=site,
                                               systemprod=syp)

                parcel.urls.add(url)
                parcel.save()

                for b in range(randrange(3)):
                    block = Block.objects.create(name=f.word(),
                                                 parcel=parcel,
                                                 surface=randrange(20),
                                                 date_debut=f.date_time(),
                                                 date_fin=f.date_time(),
                                                 usage=f.word(),
                                                 center=center,
                                                 comment=" ".join(f.words(180)))

                    block.projets.add(projet)
                    block.save()


        print 'Blocks {}'.format(Block.objects.all().count())
