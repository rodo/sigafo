#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013-2016 Rodolphe Quiédeville <rodolphe@quiedeville.org>
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
"""
Une fois l'import effectue il faut mettre a jour la base avec les
commandes SQL suivantes :


sigafo=# update parc_site set map_public_info = properties  where id > 355;
sigafo=# update parc_site set parc_json = map_public_info::json where id > 355;

"""
import sys
import csv
import re
from django.contrib.gis.geos import Point
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from sigafo.map.models import Map
from sigafo.parc.models import Parcel, Block, Site, Observation
from sigafo.agrof.models import Amenagement
from sigafo.contact.models import Contact
from sigafo.projet.models import Projet
from sigafo.referentiel import models as refs
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


        make_option("-t",
                    "--truncate",
                    dest="truncate",
                    action="store_true",
                    help="truncate datas before import",
                    default=False),
        )

    def handle(self, *args, **options):
        """
        Make
        """
        if not options['filename']:
            print "-f is missing"
            sys.exit(1)

        if options['truncate']:
            Amenagement.objects.all().delete()
            Block.objects.all().update(nb_amg=0)

        i = 0
        ok = 0
        with open(options['filename'], 'rb') as f:
                reader = csv.reader(f)
                for row in reader:
                    i = i + 1
                    print "row %s" % i
                    if i > 3:
                        res = iline(row, i)
                        if res == 0:
                            ok = ok + 1

        print "%s on %s lines imported" % (ok, i)

        for model in [Map, Block, Parcel, Site, Amenagement, refs.AmEssence]:
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

def iline(row, i):
    res = 0
    block_center = None
    projets = []
    data_imports = {}
    r = 0
    for data in row:
        data_imports['col%d' % (r)] = data
        r = r + 1

    site_nom = row[0].strip()
    am_nom = row[1].strip()
    block_nom = row[2].strip()    

    block_ids = Block.objects.filter(
        name=block_nom,
        parcel__site__name=site_nom)

    if len(block_ids) != 1:
        return 0

    # E - 4
    # F - 5
    # G - 6
    nature = row[6].strip()
    (nat_id, created) = refs.AmNature.objects.get_or_create(name=nature)

    # Objet amenagement
    am = Amenagement.objects.create(name=am_nom, block=block_ids[0])

    # H - 7
    # I - 8
    # J - 9
    # K - 10
    essences = [e.strip() for e in (row[10].strip()).split(';')]
    for ess in essences:
        essc = unicode(ess,"UTF-8")
        essc = essc.replace(u"\xc2\xa0", " ")
        essc = essc.strip()
        if len(essc):
            (essence, created) = refs.AmEssence.objects.get_or_create(
                name=essc.capitalize())
            if created:
                essence.comment = ess
                essence.save()
                print ess
            am.essences.add(essence)


    # L - 11
    conduites = [e.strip() for e in (row[11].strip()).split(';')]
    for cond in conduites:
        if len(cond):
            (conduite, created) = refs.AmConduite.objects.get_or_create(name=cond.capitalize())
            am.conduites.add(conduite)
    #

    # M 12
    # N 13
    # O 14
    # P 15 : density
    try:
        am.density = float(row[15])
    except:
        pass
    # Q 16
    # R 17
    try:
        am.dist_inter_line = float(row[17])
    except:
        pass
    

    am.nature = nat_id
    am.save()



    return res
