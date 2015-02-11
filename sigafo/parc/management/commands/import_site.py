#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013-2015 Rodolphe Quiédeville <rodolphe@quiedeville.org>
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
#
# Field delimiter : "," coma
#
import sys
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
import json


class Command(BaseCommand):
    help = 'Import datas'
    option_list = BaseCommand.option_list + (
        make_option("-f",
                    "--filename",
                    dest="filename",
                    type="string",
                    help="number of values to input",
                    default=None),

        make_option("-p",
                    "--projet",
                    dest="projet",
                    type="string",
                    help="number of values to input",
                    default=None),
        )

    def handle(self, *args, **options):
        """
        Make
        """
        if not options['filename']:
            print "-f is missing"
            sys.exit(1)

        if not options['projet']:
            print "-p [PROJET_ID] is missing"
            sys.exit(1)

        i = 0
        ok = 0
        with open(options['filename'], 'rb') as f:
                reader = csv.reader(f)
                for row in reader:
                    i = i + 1
                    if i > 3:
                        res = iline(row, i, options['projet'])
                        if res == 0:
                            ok = ok + 1

        print "%s on %s lines imported" % (ok, i)

        for model in [Map, Block, Parcel, Site, Amenagement]:
            print "%s %d" % (model, model.objects.all().count())

# def clean_all():
#     """
#     """
#     for model in [Map, Block, Parcel, Site, Amenagement]:
#         model.objects.all().delete()

def clean(value):

    value = value.strip()
    if value == 'NR' or value == 'NC':
        value = None

    if value == 'Aucun' or value == 'Aucune':
        value = None

    return value

def iline(row, i, projet_id):
    res = 0
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
        (lastname, firstname) = (name[0], name[1])
        block_name = row[3]

        # coord 49° 7' 3.529" N     1° 43' 44.987" E
        coord = row[1]

    except:
        print "Parsing error line %d : %s"% (i, row[0])


    for proj in row[27].strip().split(';'):
        if len(proj):
            projets.append(proj.strip())


    print firstname,lastname

    try:
        objcontact = Contact.objects.filter(firstname=firstname,
                                            lastname=lastname)
        email = objcontact[0].email
    except:
        email=""

    


    town = row[4].strip()
    contact = row[2].strip()

    try:
        surface = float(row[5])
    except:
        surface = None

    lat = None
    lon = None
    matchObj = re.match(r'^(\d+).*(\d+)..(\d+\.\d+).\s?(\w).*(\d+).*(\d+)..(\d+\.\d+).\s?(\w)', row[1])
    if matchObj:
        try:
            lat = float(matchObj.group(1)) + float(matchObj.group(2))/60 + float(matchObj.group(3))/3600
            if matchObj.group(4) == "S":
                lat = 0 - lat
            lon = float(matchObj.group(5)) + float(matchObj.group(6))/60 + float(matchObj.group(7))/3600
            if matchObj.group(8) == "W":
                lon = 0 - lon

            print "latitude : %s lon %s %s " % (str(lat), str(lon), row[1])
        except:
            print 'bad coord'

    coord = row[1].strip()
    lat = float(coord.split(',')[0])
    lon = float(coord.split(',')[1])

    print 'lat : %s, lon: %s' % (lat, lon)

    wp = row[12].strip()
    url = row[13].strip()
    quality = row[3].strip()
    stkholdergroup = 17

    image = "http://www.agforward.eu/%s" % (row[45].strip())

    proper = {'url': url,
              'import': 'import_janvier_20125',
              'agforward_class': row[12].strip(),
              'latitude': lat,
              'longitude': lon,
              'contact': contact,
              'email': email,
              'town': town,
              'wp': wp,
              'image': image,
              'imgheight': 82,
              'imgwidth': 198,
              'stkgroup': stkholdergroup}

    site = Site.objects.create(name=site_nom,
                               properties=proper)

    #print site.properties

    print email

    if lat and lon:
        site.center = Point(lon, lat)
        site.save()
    #

    proj = Projet.objects.get(pk=projet_id)
    site.projets.add(proj)
    return res
