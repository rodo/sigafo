#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 Rodolphe Quiédeville <rodolphe@quiedeville.org>
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
import requests
from tempfile import NamedTemporaryFile
from django.core.management.base import BaseCommand
from optparse import make_option
from faker import Faker
from django.db import connection


class Command(BaseCommand):
    help = 'Import datas'
    option_list = BaseCommand.option_list + (
        make_option("-n",
                    "--nbvalues",
                    dest="nbvalues",
                    type="int",
                    help="number of values to input",
                    default=10),
        )

    def handle(self, *args, **options):
        """
        Make
        """
        url = "http://oapi-fr.openstreetmap.fr/oapi/interpreter?data=[out:json];relation[%22ref:NUTS%22~%22^FR.*%22][%22admin_level%22=%226%22];out;%3E%3E;out%20skel;"

        fpath = NamedTemporaryFile(delete=False)
        print fpath.name
        print download(url, fpath)

def download(url, fpath, verbose=False):
    """Download a file

    url (string) : URL
    fpath (string) : file path where to store the file
    """
    result = None
    try:
        r = requests.get(url, timeout=10, headers=readheader())
        if r.status_code == 200:
            if verbose:
                msg = "size %d\n" % (int(r.headers['content-length']))
                sys.stdout.write(msg)
            f = fpath
            for chunk in r.iter_content(chunk_size=512 * 1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
            f.close()
        result = r.status_code
    except:
        pass
    return result, fpath

def readheader():
    try:
        trouble = 'In case of trouble contact {}'.format(environ['DEBEMAIL'])
        headers = {'User-Agent': trouble}
    except:
        headers = {'User-Agent': 'python/requests'}

    return headers
