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
from rest_framework import serializers
from rest_framework import permissions
from rest_framework import viewsets
from sigafo.referentiel import models
from sigafo.referentiel import serializers
from sigafo.utils.view_mixins import APICacheMixin


class ApiV1Views(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    paginate_by = 10


class AmEssenceViewSet(ApiV1Views):
    queryset = models.AmEssence.objects.all()
    serializer_class = serializers.AmEssenceSerializer


class AmConduiteViewSet(ApiV1Views):
    queryset = models.AmConduite.objects.all()
    serializer_class = serializers.AmConduiteSerializer


class AmNatureViewSet(ApiV1Views):
    queryset = models.AmNature.objects.all()
    serializer_class = serializers.AmNatureSerializer


class AmObjectifInitViewSet(ApiV1Views):
    queryset = models.AmObjectifInit.objects.all()
    serializer_class = serializers.AmObjectifInitSerializer


class AmNaturebeViewSet(ApiV1Views):
    queryset = models.AmNaturebe.objects.all()
    serializer_class = serializers.AmNaturebeSerializer


class AmGestionbeViewSet(ApiV1Views):
    queryset = models.AmGestionbe.objects.all()
    serializer_class = serializers.AmGestionbeSerializer


class TopographyViewSet(ApiV1Views):
    queryset = models.Topography.objects.all()
    serializer_class = serializers.TopographySerializer
