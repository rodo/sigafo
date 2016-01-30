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
# sigafo/referentiel
#
from django.contrib import admin
from sigafo.referentiel import models

admin.site.register(models.SystemProd)
admin.site.register(models.AnimalProduction)
admin.site.register(models.VegetalProductionAnnual)
admin.site.register(models.VegetalProductionPerennial)
admin.site.register(models.Topography)
admin.site.register(models.Texture)
admin.site.register(models.ClassePH)
admin.site.register(models.ClasseProfondeur)
admin.site.register(models.ClasseHumidity)


class AmEssenceAdmin(admin.ModelAdmin):
    """Custom Admin for essences
    """
    ordering = ['name']

admin.site.register(models.AmEssence, AmEssenceAdmin)
