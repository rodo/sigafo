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
from sigafo.referentiel import models


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
