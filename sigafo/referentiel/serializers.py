# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 Rodolphe Quiédeville <rodolphe@quiedeville.org>
# Copyright (c) 2014 Agroof <http://www.agroof.net/>
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
from rest_framework import serializers
from rest_framework import permissions
from rest_framework import viewsets

from sigafo.referentiel import models

# Serializers define the API representation.
class AmConduiteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.AmConduite
        fields = ('uuid', 'name')


class AmEssenceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.AmEssence
        fields = ('uuid', 'name')
        

class AmNatureSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.AmNature
        fields = ('uuid', 'name')


class AmObjectifInitSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.AmObjectifInit
        fields = ('uuid', 'name')

class AmProtectionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.AmProtection
        fields = ('uuid', 'name')


class AmPaillageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.AmPaillage
        fields = ('uuid', 'name')
        

class AmGestionbeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.AmGestionbe
        fields = ('uuid', 'name')


class AmNaturebeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.AmNaturebe
        fields = ('uuid', 'name')


class TopographySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Topography
        fields = ('uuid', 'name')


class AnimalProductionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.AnimalProduction
        fields = ('uuid', 'name')


class VegetalProductionAnnualSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.VegetalProductionAnnual
        fields = ('uuid', 'name')
