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
import csv
import re
from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand
from sigafo.parc.models import Champ, Parcel, Site
from sigafo.agrof.models import Essence, Peuplement
from sigafo.contact.models import Contact
from sigafo.projet.models import Projet
from optparse import make_option
from faker import Faker
from django.db import connection


class Command(BaseCommand):
    help = 'Import datas'
    option_list = BaseCommand.option_list + (
        make_option("-f",
                    "--filename",
                    dest="filename",
                    type="string",
                    help="number of values to input",
                    default=None),
        )

    def handle(self, *args, **options):
        """
        Make
        """
        clean_all()

        if not options['filename']:
            print "-f is missing"
            sys.exit(1)

        i = 0
        ok = 0
        with open(options['filename'], 'rb') as f:
                reader = csv.reader(f)
                for row in reader:
                    i = i + 1
                    if i > 1:
                        res = iline(row, i)
                        if res == 0:
                            ok = ok + 1

        print "%s on %s lines imported" % (ok, i)


def clean_all():
    """
    """
    Parcel.objects.all().delete()
    Champ.objects.all().delete()
    Site.objects.all().delete()
    Contact.objects.all().delete()
    Peuplement.objects.all().delete()
    Projet.objects.all().delete()

def iline(row, i):
    agroof_users = [1,2,3,4]
    res = 1
    bloc_center = None
    projets = []

    try:
        name = row[0].split(' ')
        (firstname, lastname) = (name[0], name[1])
        parcel_name = row[3]
        
        # coord 49° 7' 3.529" N     1° 43' 44.987" E 
        coord = row[9]
        for proj in row[27].strip().split(';'):
            if len(proj):
                projets.append(proj.strip())
    except:
        print "Parsing error line %d : %s"% (i, row[0])

    matchObj = re.match(r'^(\d+).*(\d+)..(\d+\.\d+).\s(\w).*(\d+).*(\d+)..(\d+\.\d+).\s(\w)', row[9])
    if matchObj:
        try:
            lat = float(matchObj.group(1)) + float(matchObj.group(2))/60 + float(matchObj.group(3))/3600
            if matchObj.group(4) == "S":
                lat = 0 - lat
            lon = float(matchObj.group(5)) + float(matchObj.group(6))/60 + float(matchObj.group(7))/3600
            if matchObj.group(8) == "W":
                lon = 0 - lon

            bloc_center = Point(12.4604, 43.9420)
            print "latitude : %s lon %s " % (str(lat), str(lon))
        except:
            print 'bad coord'

    try:        
        site = Site.objects.create(name=parcel_name)

        champ = Champ.objects.create(site=site,
                                     name=parcel_name)
    
        parcel = Parcel.objects.create(name=parcel_name,
                                       champ=champ,
                                       center=bloc_center)
        #                                   surface=f.pyfloat(),
        #                                   date_debut=f.date_time(),
        #                                   date_fin=f.date_time(),
        #                                   usage=f.word())    
        res = 0
    except:
        print "error line %d"% (i)

    if res == 0:
        for projname in projets:
            p, created = Projet.objects.get_or_create(name=projname)
            if created:
                p.users.add(1)
                p.save()
            parcel.projet.add(p)
            parcel.save()

    return res
