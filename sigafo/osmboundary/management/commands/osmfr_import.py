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
# Import shapefiles from https://www.data.gouv.fr/fr/datasets/contours-des-departements-francais-issus-d-openstreetmap/
#
#
import sys
import os
import time

from tempfile import NamedTemporaryFile
from django.core.management.base import BaseCommand
from optparse import make_option
from faker import Faker
from django.db import connection
from django.contrib.gis.utils import LayerMapping
from sigafo.osmboundary.models import Departement


class Command(BaseCommand):
    help = 'Import datas'
    option_list = BaseCommand.option_list + (
        make_option("-f",
                    "--fpath",
                    dest="fpath",
                    type="string",
                    help="filepath to import",
                    default=None),
        )

    def handle(self, *args, **options):
        """
        Make
        """
        from django.contrib.gis.gdal import DataSource
        ds = DataSource(options['fpath'])
        print(ds)
        if len(ds) == 1:
            lyr = ds[0]
        print lyr.geom_type, lyr.fields

        world_mapping = {
            'code_insee' : 'code_insee',
            'nuts3' : 'nuts3',
            'name' : 'nom',
            'polygon' : 'polygon',
            }


        lm = LayerMapping(Departement, options['fpath'], world_mapping,
                          transform=False, encoding='iso-8859-1')

        lm.save(strict=True, verbose=True)
