# -*- coding: utf-8 -*-
#
# Copyright (c) 2014,2015 Rodolphe Quiédeville <rodolphe@quiedeville.org>
# Copyright (c) 2014,2015 Agroof <http://www.agroof.net/>
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
from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from .models import Map
from .models import ModelProperty


class MapAdmin(LeafletGeoAdmin):
    readonly_fields = ('center',)
    list_display = ['title']

class ModelPropertyAdmin(admin.ModelAdmin):
    list_display = ['model', 'name', 'key']
    ordering = ["model"]
    list_filter = ('model',)

admin.site.register(Map, MapAdmin)
admin.site.register(ModelProperty, ModelPropertyAdmin)
