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
from sigafo.contact.models import Contact, Organisme
from sigafo.projet.models import Projet, Thematique, Comment
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
        print "Orga %d " % (Organisme.objects.all().count())

def clean_all():
    """
    """
    Comment.objects.all().delete()
    Organisme.objects.all().delete()
    Contact.objects.all().delete()
    Projet.objects.all().delete()

def iline(row, i):

    projet_name = row[0]
    taxon = row[1]
    r_part = row[2]
    financ = row[3]
    r_contact = row[4]
    referent = row[11]

    if taxon == 'Recherche':
        taxon = 0
    elif taxon == 'Territoire':
        taxon = 1
    else:
        taxon = None

    contacts = []
    partenaires = []
    financeurs = []
    thematiques = []

    for conname in r_contact.split(';'):
        contact, created = Contact.objects.get_or_create(firstname=conname.split(' ')[1].strip(),
                                                         lastname=conname.split(' ')[0].strip())
        contacts.append(contact)
    
    for tname in row[8].split(';'):
        thematique, created = Thematique.objects.get_or_create(name=tname.strip())
        thematiques.append(thematique)

    for finname in financ.split(';'):
        financeur, created = Organisme.objects.get_or_create(name=finname.strip())
        financeurs.append(financeur)

    for partname in r_part.split(';'):
        partenaire, created = Organisme.objects.get_or_create(name=partname.strip())
        partenaires.append(partenaire)

    firstname = referent.split(' ')[1].strip()
    lastname = referent.split(' ')[1].strip()

    referent, created = Contact.objects.get_or_create(firstname=firstname, lastname=lastname)

    user, created = User.objects.get_or_create(first_name=firstname,
                                               last_name=lastname,
                                               username=firstname.lower())
    referent.user = user
    referent.save()

    projet = Projet.objects.create(name=projet_name.strip(),
                                   taxon=taxon,
                                   referent_interne=user,
                                   annee_debut=int(row[5]),
                                   annee_fin=int(row[6]),
                                   objectifs=row[7].strip())

    for p in partenaires:
        projet.partenaires.add(p)

    for f in financeurs:
        projet.financeurs.add(f)

    for c in contacts:
        projet.coordinators.add(c)

    for t in thematiques:
        projet.thematiques.add(t)


    c = row[10]
    c = c.strip()
    if len(c) > 0:
        Comment.objects.create(comment=c,
                               projet=projet)

    c = row[9]
    c = c.strip()
    if len(c) > 0:
        print c
        projet.url = c
        projet.save()






    return 1
