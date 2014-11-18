# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Rodolphe Quiédeville <rodolphe@quiedeville.org>
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
from django import forms
from django.forms.widgets import Textarea, TextInput, Select, CheckboxInput, HiddenInput, RadioSelect
from sigafo.map import models
from sigafo.projet.models import Projet
from crispy_forms.helper import FormHelper
from crispy_forms import layout
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions, InlineRadios

xlarge = {'class': 'form-control'}
large = {'class': 'form-control'}
standard = {'class': 'form-control'}
date = {'class': 'datepicker'}


class MapForm(forms.ModelForm):
    """
    Use to create Experience
    """
    class Meta(object):
        model = models.Map
        # user will be set in views.ResumeNew
        # other fields will be set as model default
        exclude = ('creator', 'properties', 'center')
      
    title = forms.CharField(max_length=50,
                            required=True,
                            label=u"Titre",
                            widget=TextInput(attrs=xlarge))

    projets = forms.ModelMultipleChoiceField(queryset=Projet.objects.all().order_by('name'))

    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-lg-2'
    helper.field_class = 'col-lg-10'
    helper.layout = layout.Layout(
        layout.Field('title'),
        layout.Field('projets'),
        FormActions(
            layout.Submit('save_changes', 'Enregistrer', css_class="btn-primary"),
            layout.Submit('cancel', 'Annuler', css_class="btn-danger"),
            )
        )
