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
from .models import Projet, Thematique, Comment


class ProjetAdmin(admin.ModelAdmin):
    list_display = ['name', 'annee_debut', 'annee_fin']

class ThematiqueAdmin(admin.ModelAdmin):
    ordering = ['name']

class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'creation', 'abstract']
    ordering = ['-creation']


admin.site.register(Projet, ProjetAdmin)
admin.site.register(Thematique, ThematiqueAdmin)
admin.site.register(Comment, CommentAdmin)
