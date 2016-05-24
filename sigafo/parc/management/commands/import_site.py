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

        make_option("-p",
                    "--projet",
                    dest="projet",
                    type="string",
                    help="project id to link on",
                    default=None),

        make_option("-c",
                    "--code",
                    dest="code_projet",
                    type="string",
                    help="project code found in .ods data file",
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
            Block.objects.all().delete()
            Parcel.objects.all().delete()
            Site.objects.all().delete()

        i = 0
        ok = 0
        with open(options['filename'], 'rb') as f:
                reader = csv.reader(f)
                for row in reader:
                    i = i + 1
                    print "row %s" % i
                    if i > 3:
                        res = iline(row, i, options['projet'], options['code_projet'])
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

def iline(row, i, projet_id, project_code):
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
        print firstname,lastname
    except:
        print "Parsing error line %d : %s"% (i, row[0])

    # filtre sur la colonne projet AR des blocs
    projs = row[43].strip().split(';')
    cprojs = [f.strip() for f in projs]
    for proj in cprojs:
        try:
            if len(proj):
                (projet_id, created) = Projet.objects.get_or_create(name=proj,
                                                                    code=proj,
                                                                    taxon=1)
                projets.append(projet_id.id)
        except:
            pass

    try:
        objcontact = Contact.objects.filter(firstname=firstname,
                                            lastname=lastname)
        email = objcontact[0].email
    except:
        objcontact = None
        email=""

    town = row[4].strip()
    contact = row[2].strip()

    # icon_url colonne AV : 47
    icon_url = row[47].strip()

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
    slat = unicode(coord.split(',')[0],"UTF-8")
    slat = slat.replace(u"\xc2\xa0", " ")
    lat = float(slat)
    slon = unicode(coord.split(',')[1],"UTF-8")
    slon = slon.replace(u"\xc2\xa0", " ")
    lon = float(slon)

    print 'lat : %s, lon: %s' % (lat, lon)

    commune = row[4].strip()

    wp = row[12].strip()
    url = row[13].strip()
    quality = row[3].strip()
    stkholdergroup = 17

    field = row[35].strip()

    # AT
    #image = "http://www.agforward.eu/%s" % (row[45].strip())
    image = row[45].strip()

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
              'stkgroup': stkholdergroup,
              'icon_url': icon_url}


    (site, created) = Site.objects.get_or_create(name=site_nom,
                                                 center = Point(lon, lat))

    if len(commune):
        site.commune = commune

    # Site referent
    if objcontact is not None:
        site.referent = objcontact[0]

    if created:
        site.properties=proper
        site.save()

    #print site.properties

    print site.id, email

    if lat and lon:
        site.center = Point(lon, lat)
        site.save()
    #
    # Parcelles
    # G  6 Nom
    parcel_nom = row[6].strip()

    if parcel_nom == "":
        parcel_nom = "Parcelle sans nom"

    # H  7
    # I  8
    # J  9
    # K 10
    # L 11 System Prod
    systemprod = row[11].strip()
    # M 12
    workgroup = row[12].strip()
    # N 13
    workgroup_url = row[13].strip()

    # O 14 - Coord GPS
    coord = row[14].strip()
    slat = unicode(coord.split(',')[0],"UTF-8")
    slat = slat.replace(u"\xc2\xa0", " ")
    lat = float(slat)
    slon = unicode(coord.split(',')[1],"UTF-8")
    slon = slon.replace(u"\xc2\xa0", " ")
    lon = float(slon)

    (parcel, created) = Parcel.objects.get_or_create(
        name=parcel_nom,
        site=site,
        center = Point(lon, lat),
        creator=User.objects.get(pk=1))

    if len(systemprod) > 0 and len(systemprod) < 301:
        (obj, created) = refs.SystemProd.objects.get_or_create(name=systemprod.capitalize())
        parcel.systemprod = obj

    if len(workgroup):
        parcel.workgroup = workgroup

    if len(workgroup_url):
        parcel.workgroup_url = workgroup_url

    # P 15
    # Q 16 - Expe
    # R 17
    # S 18 - Dispositif experimental
    expedevs = [e.strip() for e in (row[18].strip()).split(';')]
    for tilg in expedevs:
        if len(tilg) > 0 and len(tilg) < 301:
            (expedev, created) = refs.ExperimentalDevice.objects.get_or_create(name=tilg.capitalize())
            parcel.experimental_devices.add(expedev)
    #
    # T 19
    # U 20

    # surface colonne K
    try:
        parcel.surface = float(row[10].strip())
    except:
        pass

    try:
        parcel.altitude = float(row[15].strip())
    except:
        pass

    try:
        if row[16].strip() == 'Oui':
            parcel.experimental = True
    except:
        pass

    parcel.icon_url = icon_url

    parcel.save()
    #
    # Bloc
    #
    # V 21 Nom
    bloc_nom = row[21].strip()

    if bloc_nom == "":
        bloc_nom = "Sans nom"

    (bloc, created) = Block.objects.get_or_create(name=bloc_nom,
                                                  parcel=parcel
                                                  )
    # W 22 Nature du block
    natures = [e.strip() for e in (row[22].strip()).split(';')]
    for nat in natures:
        if len(nat):
            (nature, created) = refs.NatureBlock.objects.get_or_create(name=nat.capitalize())
            bloc.nature.add(nature)

    # X 23
    # Y 24
    # Z 25

    try:
        coord = row[25].strip()
        lat = float(coord.split(',')[0])
        lon = float(coord.split(',')[1])
        bloc.center = Point(lon, lat)
    except:
        pass

    # sometimes bloc has no coords
    if bloc.center is None:
        bloc.center = parcel.center


    properties = {'surface': row[24].strip(),
                  'topography': row[28].strip(),
                  'texture': row[29].strip(),
                  'classe_ph': row[30].strip(),
                  'classe_profondeur': row[31].strip(),
                  'humidity': row[32].strip(),
                  'drainage': row[33].strip(),
                  'irrigation': row[34].strip(),
                  'prod_veg_an': row[35].strip(),
                  'prod_veg_per': row[36].strip(),
                  'prod_animal': row[37].strip(),
                  'facon_culturale': row[38].strip(), # AM
                  'fertilisation': row[39].strip(), # AN
                  'traitement_phyto': row[40].strip(), # AO
                  'mode_conduite': row[41].strip(), # AP
                  'projets': row[43].strip(), # AR
                  'image_url': row[45].strip(), # AT
                  'icon_url': row[47].strip(), # AV
                  }

    # AA annee de debut
    if len(row[26]):
        try:
            bloc.year_start = int(row[26])
        except:
            pass
    # AB annee de fin
    if len(row[27]):
        try:
            bloc.year_start = int(row[27])
        except:
            pass

    # AC topography
    # AD texture

    # AE
    classe_ph = row[30].strip()
    if len(classe_ph):
        if (classe_ph != 'NR'):
            (PH, created) = refs.ClassePH.objects.get_or_create(name=classe_ph)
            bloc.classeph = PH

    classe_prof = row[31].strip()
    if len(classe_prof):
        if (classe_prof != 'NR'):
            (PROF, created) = refs.ClasseProfondeur.objects.get_or_create(name=classe_prof)
            bloc.classeprof = PROF

    classe_humid = row[32].strip()
    if len(classe_humid):
        if (classe_humid != 'NR'):
            (HUMID, created) = refs.ClasseHumidity.objects.get_or_create(name=classe_humid)
            bloc.classehumidity = HUMID


    bloc.prod_veg_an = row[35].strip()
    bloc.prod_veg_per = row[36].strip()
    bloc.prod_animal = row[37].strip()

    # Façons culturales / Tillage
    tillages = [e.strip() for e in (row[38].strip()).split(';')]
    for tilg in tillages:
        if len(tilg):
            (tillage, created) = refs.Tillage.objects.get_or_create(name=tilg.capitalize())
            bloc.tillages.add(tillage)
    #

    # AP 41
    # Mode de conduites
    conduites = [e.strip() for e in (row[41].strip()).split(';')]
    for tilg in conduites:
        if len(tilg):
            (conduite, created) = refs.ModeConduite.objects.get_or_create(name=tilg.capitalize())
            bloc.conduites.add(conduite)
    #

    # AQ 42
    # AR 43
    # AS 44
    # AT 45

    bloc.properties = properties
    bloc.save()

    # Ajout aux projets
    for proj in projets:
        proj = Projet.objects.get(pk=proj)
        bloc.projets.add(proj)

    return res
