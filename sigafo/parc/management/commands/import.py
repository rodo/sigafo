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

        for model in [Map, Block, Parcel, Site, Amenagement]:
            print "%s %d" % (model, model.objects.all().count())

def clean_all():
    """
    """
    for model in [Map, Block, Parcel, Site, Amenagement]:
        model.objects.all().delete()

def clean(value):

    value = value.strip()
    if value == 'NR' or value == 'NC':
        value = None

    if value == 'Aucun' or value == 'Aucune':
        value = None

    return value

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

    lat = None
    lon = None
    matchObj = re.match(r'^(\d+).*(\d+)..(\d+\.\d+).\s?(\w).*(\d+).*(\d+)..(\d+\.\d+).\s?(\w)', row[12])
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
    #
    models.ClasseProfondeur.objects.all().delete()
    models.ClasseProfondeur.objects.get_or_create(name='Hétérogène')
    models.ClasseProfondeur.objects.get_or_create(name='0 - 50 cm')
    models.ClasseProfondeur.objects.get_or_create(name='50 - 100 cm')
    models.ClasseProfondeur.objects.get_or_create(name='> 100 cm')
    models.ClasseHumidity.objects.all().delete()
    models.ClasseHumidity.objects.get_or_create(name='Humide')
    models.ClasseHumidity.objects.get_or_create(name='Très humide')
    models.ClasseHumidity.objects.get_or_create(name='Sèche')
    models.ClassePH.objects.all().delete()
    models.ClassePH.objects.get_or_create(name='4 - 4,5')
    models.ClassePH.objects.get_or_create(name='4,5 - 5')
    models.ClassePH.objects.get_or_create(name='5 - 5,5')
    models.ClassePH.objects.get_or_create(name='5,5 - 6')
    models.ClassePH.objects.get_or_create(name='6 - 6,5')
    models.ClassePH.objects.get_or_create(name='6,5 - 6')
    models.ClassePH.objects.get_or_create(name='7 - 7,5')
    models.ClassePH.objects.get_or_create(name='7,5 - 8')
    models.ClassePH.objects.get_or_create(name='8 - 8,5')
    models.ClassePH.objects.get_or_create(name='8,5 - 9')
    models.ClassePH.objects.get_or_create(name='9 - 9,5')
    models.ClassePH.objects.get_or_create(name='9,5 - 10')
    models.ClassePH.objects.get_or_create(name='10 - 10,5')

    # parcel
    #
    parcel_name = row[6].strip()
    system = row[11].strip()
    coord = row[12].strip()

    system, created = models.SystemProd.objects.get_or_create(name=system)

    parcel, created = Parcel.objects.get_or_create(site=site,
                                                   name=parcel_name,
                                                   systemprod=system,                                                   
                                                   center=block_center)

    if lat and lon:
        parcel.center = Point(lon, lat)
        parcel.save()

    #
    #
    block_name = row[17].strip()
    r_surface = clean(row[20])
    r_topo = row[24].strip()
    r_klassph = clean(row[26])
    r_klassprof = clean(row[27])
    r_klasshumid = clean(row[28])
    comment = row[30].strip()
    projets = row[39]
    #
    topo, created = models.Topography.objects.get_or_create(name=r_topo)

    try:
        surface=float('.'.join(r_surface.split(',')))
    except:
        surface = None

    # klasse de PH
    klassph = None
    klassprof = None
    klasshumid = None
    if r_klassph:
        klassph, created = models.ClassePH.objects.get_or_create(name=r_klassph)

    if r_klassprof:
        klassprof, created = models.ClasseProfondeur.objects.get_or_create(name=r_klassprof)

    if r_klasshumid:
        klasshumid, created = models.ClasseHumidity.objects.get_or_create(name=r_klasshumid)

    #klassph = None
    #klassprof = None
    #klasshumid = None

    print "%d %s" % (Block.objects.all().count(), klassph)
    print "%s %s %s" % (klassph, klassprof, klasshumid)

    block = Block.objects.create(name=block_name,
                                 parcel=parcel,
                                 topography=topo,
                                 center=block_center,
                                 import_initial=data_imports)


    block.classph=klassph
#    block.save()


    if surface:
        block.surface = surface
        block.save()


    print "block %d ok" % (block.id)

    for p in projets.split(';'):
        projet = None
        try:
            projet = Projet.objects.get(name=p.strip())
        except:
            print "erreur projet inconnu '%s'" % (p.strip())

    if projet:
        block.projets.add(projet)

    if len(comment) > 1000:
        Observation.objects.create(author=User.objects.get(pk=1),
                                   date_observation='1970-01-01',
                                   block=block,
                                   observation=comment,
                                   comment="commentaire présent dans le fichier excel")

    return res
