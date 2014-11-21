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
# sigafo/parc
#
from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from .models import Parcel, Block, Site

class ParcelAdmin(LeafletGeoAdmin):
    """Custom Admin for parcels
    """
    readonly_fields = ('nb_block',)
    list_display = ('name', 'site', 'nb_block')
    list_filter = ('site', 'systemprod')
    ordering = ['site', 'name']

class SiteAdmin(LeafletGeoAdmin):
    """Custom Admin for sites
    """
    search_fields = ('name',)
    readonly_fields = ('nb_block','nb_parcel')
    list_display = ('name', 'address')
    ordering = ['name']


class BlockAdmin(LeafletGeoAdmin):
    """Custom Admin for blocks
    """
    search_fields = ('name',)
    readonly_fields = ('import_initial',)
    list_display = ('name', 'parcel')
    ordering = ['parcel']

admin.site.register(Parcel, ParcelAdmin)
admin.site.register(Block, BlockAdmin)
admin.site.register(Site, SiteAdmin)
