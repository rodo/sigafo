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
import csv
from django.core.management.base import BaseCommand
from sigafo.contact.models import Contact, Organisme
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
        if not options['filename']:
            print "-f is missing"
            sys.exit(1)

        i = 0
        ok = 0
        with open(options['filename'], 'rb') as f:
                reader = csv.reader(f)
                for row in reader:
                    i = i + 1
                    if i > 2:
                        res = iline(row, i, options['filename'])
                        if res == 0:
                            ok = ok + 1

        print "%s on %s lines imported" % (ok, i)


def cleanr(txt):
    if txt == 'NR':
        return ""
    else:
        return txt

def iline(row, i, importfile):
    """
    0             1         2    3                    4           5       6       7         8
    "Nom, prénom",Organisme,Pays,Département/province,Code postal,Commune,Adresse,Téléphone,Mail
    """

    conname = row[0].strip()
    organism = row[1].strip()
    pays = row[2].strip().strip()
    departement = row[3].strip().strip()
    cp = row[4].strip().strip()
    commune = row[5].strip().strip()
    address = row[6].strip().strip()
    phonenumber = cleanr(row[7].strip())
    email = cleanr(row[8].strip())

    try:
        firstname=conname.split(' ')[1].strip()
        lastname=conname.split(' ')[0].strip()
    except:
        lastname=conname
        firstname=''

    properties = {'import_file': importfile,
                  'name': conname,
                  'organism': organism,
                  'pays': pays,
                  'departement': departement,
                  'cp': cp,
                  'commune': commune,
                  'address': address,
                  'phonenumber': phonenumber,
                  'email': email}

    fulladdress = "%s\n%s %s\n%s\n%s" % (address, cp, commune, departement, pays)

    organism, created = Organisme.objects.get_or_create(name=organism)

    contact, created = Contact.objects.get_or_create(firstname=firstname,
                                                     lastname=lastname,
                                                     address=fulladdress.strip(),
                                                     email=email,
                                                     phonenumber=phonenumber
                                                     )

    if created:
        contact.properties = properties
        contact.save()

        organism.contacts.add(contact)

        return 0
    else:
        return 1
