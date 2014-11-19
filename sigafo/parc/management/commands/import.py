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
from sigafo.referentiel import models
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
                    if i > 3:
                        res = iline(row, i)
                        if res == 0:
                            ok = ok + 1

        print "%s on %s lines imported" % (ok, i)

        for model in [Map, Block, Parcel, Site]:
            print "%s %d" % (model, model.objects.all().count())




def clean_all():
    """
    """
    Map.objects.all().delete()
    Block.objects.all().delete()
    Parcel.objects.all().delete()
    Site.objects.all().delete()
    Amenagement.objects.all().delete()


def iline(row, i):
    res = 1
    block_center = None
    projets = []    
    data_imports = {}
    r = 0
    for data in row:
        data_imports['col%d' % (r)] = data
        r = r + 1

    site_nom = row[0].strip()

    
    try:
        name = row[2].split(' ')
        (firstname, lastname) = (name[0], name[1])
        block_name = row[3]

        # coord 49° 7' 3.529" N     1° 43' 44.987" E
        coord = row[1]

    except:
        print "Parsing error line %d : %s"% (i, row[0])


    for proj in row[27].strip().split(';'):
        if len(proj):
            projets.append(proj.strip())

    try:
        surface = float(row[5])
    except:
        surface = None


    matchObj = re.match(r'^(\d+).*(\d+)..(\d+\.\d+).\s(\w).*(\d+).*(\d+)..(\d+\.\d+).\s(\w)', row[9])
    if matchObj:
        try:
            lat = float(matchObj.group(1)) + float(matchObj.group(2))/60 + float(matchObj.group(3))/3600
            if matchObj.group(4) == "S":
                lat = 0 - lat
            lon = float(matchObj.group(5)) + float(matchObj.group(6))/60 + float(matchObj.group(7))/3600
            if matchObj.group(8) == "W":
                lon = 0 - lon

            print "latitude : %s lon %s " % (str(lat), str(lon))
        except:
            print 'bad coord'


    site, created = Site.objects.get_or_create(name=site_nom)

    # parcel
    #
    parcel_name = row[6].strip()
    system = row[11].strip()

    system, created = models.SystemProd.objects.get_or_create(name=system)
    
    parcel, created = Parcel.objects.get_or_create(site=site,
                                                   systemprod=system,
                                                   name=parcel_name,
                                                   center=block_center)

    #
    #
    block_name = row[17].strip()
    r_topo = row[24].strip()
    comment = row[30].strip()
    projets = row[39]
    #

    topo, created = models.Topography.objects.get_or_create(name=r_topo)

    
    block = Block.objects.create(name=block_name,
                                 parcel=parcel,
                                 center=block_center,
                                 surface=surface,
                                 import_initial=data_imports)

    for p in projets.split(';'):
        projet = None
        try:
            projet, created = Projet.objects.get_or_create(name=p.strip())
        except:
            print "erreur projet inconnu '%s'" % (p.strip())

    if projet:
        block.projets.add(projet)


    if len(comment) > 0:
        Observation.objects.create(author=User.objects.get(pk=1),
                                   date_observation='1970-01-01',
                                   block=block,
                                   observation=comment,
                                   comment="commentaire présent dans le fichier excel")
        
    print "error line %d"% (i)
        

    return res
