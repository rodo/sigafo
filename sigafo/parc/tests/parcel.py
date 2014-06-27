# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Rodolphe Quiédeville <rodolphe@quiedeville.org>
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
"""
Unit tests for Resume object

"""
from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from django.db import IntegrityError
from sigafo.parc.models import Parcel


class ParcelTests(TestCase):
    """
    The main tests
    """
    def setUp(self):
        """
        set up the tests
        """
        ParcelLog.objects.all().delete()
        self.user = User.objects.create_user('foobar',
                                             'admin_search@bar.com',
                                             'admintest')



    def test_create(self):
        """
        Create a simple parcel
        """
        name = 'Senior admin'
        parcel = Parcel.objects.create(name=name,
                                       user=self.user)

        self.assertTrue(parcel.id > 0)
        self.assertEqual(parcel.status, 0)
        self.assertEqual(str(parcel), title)
        self.assertEqual(unicode(parcel), title)

