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
from django.contrib import admin
from .models import Indicator, Measure, Amenagement


class IndicatorAdmin(admin.ModelAdmin):
    fields = ('name', 'description', 'comment')


class MeasureAdmin(admin.ModelAdmin):
    list_filter = ('indicator',)


class AmenagementAdmin(admin.ModelAdmin):
    pass


admin.site.register(Indicator, IndicatorAdmin)
admin.site.register(Measure, MeasureAdmin)
admin.site.register(Amenagement, AmenagementAdmin)
