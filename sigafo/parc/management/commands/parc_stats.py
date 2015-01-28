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
from django.core.management.base import BaseCommand
from sigafo.parc.models import Parcel, Site
from sigafo.contact.models import Contact
from optparse import make_option
from faker import Faker
from django.db import connection


class Command(BaseCommand):
    help = 'Import datas'

    def handle(self, *args, **options):
        """
        Make
        """
        parcels = Parcel.objects.all().count()
        contacts = Contact.objects.all().count()
        sites = Site.objects.all().count()
        sys.stdout.write('parcels : %s\n' % (parcels))
        sys.stdout.write('contacts : %s\n' % (contacts))
        sys.stdout.write('sites : %s\n' % (sites))
                                          

