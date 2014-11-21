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
# Sigafo views for app : referentiel
#
#
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from sigafo.referentiel import models
from sigafo.referentiel import serializers
from sigafo.utils.view_mixins import APICacheMixin


class TopographyList(APICacheMixin, generics.ListAPIView):
    queryset = models.Topography.objects.all()
    serializer_class = serializers.TopographySerializer
    paginate_by = 100
