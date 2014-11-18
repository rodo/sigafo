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
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from sigafo.map.models import Map
from sigafo.parc.models import Parcel, Block, Site, Observation
from sigafo.agrof.models import Essence, Amenagement
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
    Map.objects.all().delete()
    Block.objects.all().delete()
    Parcel.objects.all().delete()
    Site.objects.all().delete()
    Contact.objects.all().delete()
    Amenagement.objects.all().delete()
    Projet.objects.all().delete()

def iline(row, i):
    agroof_users = [1,2,3,4]
    res = 1
    block_center = None
    projets = []    
    data_imports = {}
    r = 0
    for data in row:
        data_imports['col%d' % (r)] = data
        r = r + 1
    
    try:
        name = row[0].split(' ')
        (firstname, lastname) = (name[0], name[1])
        block_name = row[3]

        # coord 49° 7' 3.529" N     1° 43' 44.987" E
        coord = row[9]
        for proj in row[27].strip().split(';'):
            if len(proj):
                projets.append(proj.strip())
    except:
        print "Parsing error line %d : %s"% (i, row[0])

    try:
        surface = float(row[5])
    except:
        surface = None

    comment = row[30].strip()

    matchObj = re.match(r'^(\d+).*(\d+)..(\d+\.\d+).\s(\w).*(\d+).*(\d+)..(\d+\.\d+).\s(\w)', row[9])
    if matchObj:
        try:
            lat = float(matchObj.group(1)) + float(matchObj.group(2))/60 + float(matchObj.group(3))/3600
            if matchObj.group(4) == "S":
                lat = 0 - lat
            lon = float(matchObj.group(5)) + float(matchObj.group(6))/60 + float(matchObj.group(7))/3600
            if matchObj.group(8) == "W":
                lon = 0 - lon

            block_center = Point(12.4604, 43.9420)
            print "latitude : %s lon %s " % (str(lat), str(lon))
        except:
            print 'bad coord'


    try:
        site, created = Site.objects.get_or_create(name=block_name)

    
        parcel, created = Parcel.objects.get_or_create(site=site,
                                                       name=block_name,
                                                       center=block_center)

        block = Block.objects.create(name=block_name,
                                     parcel=parcel,
                                     center=block_center,
                                     surface=surface,
                                     import_initial=data_imports)

        if len(comment) > 0:
            Observation.objects.create(author=User.objects.get(pk=1),
                                       date_observation='1970-01-01',
                                       block=block,
                                       observation=comment,
                                       comment="commentaire présent dans le fichier excel")
        
        res = 0
    except:
        print "error line %d"% (i)

    if res == 0:
        for projname in projets:
            p, created = Projet.objects.get_or_create(name=projname)
            if created:
                p.users.add(1)
                p.save()
            block.projets.add(p)
            block.save()

    return res
