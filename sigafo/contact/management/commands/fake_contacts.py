#!/usr/bin/env python
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

import sys
import os
import time
from django.core.management.base import BaseCommand
from sigafo.parc.models import Champ, Parcel, Site
from sigafo.agrof.models import Essence, Peuplement
from sigafo.contact.models import Contact, Activite
from django.contrib.gis.geos.point import Point
from optparse import make_option
from faker import Faker
from django.db import connection


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
        Main
        """
        nbvalues = options['nbvalues']
        self.insert(nbvalues)

    def insert(self, nbvalues):
        """
        Save values in DB
        """
        f = Faker()

        while Activite.objects.all().count() < nbvalues:
            Activite.objects.create(name=f.word())

        for i in range(nbvalues):
            activite = Activite.objects.all()[i]

            site = Contact.objects.create(firstname=f.first_name(),
                                          lastname=f.last_name(),
                                          activite=activite)

