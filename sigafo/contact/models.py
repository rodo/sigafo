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
from django.db import models


class Activite(models.Model):
    """
    Activite des contacts
    agriculteurs, chercheurs
    """
    name = models.CharField(max_length=50)


class Contact(models.Model):
    """
    Contact générique
    """
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField()
    activite = models.ForeignKey(Activite)

    def __unicode__(self):
        """
        The unicode method
        """
        return u"{} {}".format(self.lastname, self.firstname)

    def __str__(self):
        """
        The string method
        """
        return "{} {}".format(self.lastname, self.firstname)
