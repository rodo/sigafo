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
from django import forms
from django.forms.widgets import Textarea, TextInput, Select, CheckboxInput, HiddenInput, RadioSelect
from sigafo.parc import models
from sigafo.referentiel import models as refs
from sigafo.projet.models import Projet
from crispy_forms.helper import FormHelper
from crispy_forms import layout
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions, InlineRadios

xlarge = {'class': 'form-control'}
large = {'class': 'form-control'}
standard = {'class': 'form-control'}
date = {'class': 'datepicker'}


class BlockForm(forms.ModelForm):
    """
    Use to edit a Block
    """
    class Meta(object):
        model = models.Block
        # user will be set in views.ResumeNew
        # other fields will be set as model default
        exclude = ('parcel',
                   'properties',
                   'variables',
                   'map_public_info',
                   'import_initial',
                   'nb_amg')

    name = forms.CharField(max_length=50,
                           required=True,
                           label=u"Name",
                           widget=TextInput(attrs=xlarge))

    projets = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Projet.objects.all().order_by('name'))

    surface = forms.CharField(required=False,
                              label=u"Surface",
                              widget=TextInput(attrs=large))
    
    prod_veg_an = forms.CharField(max_length=500,
                                  required=False,
                                  label=u"Production végétale annuelle",
                                  widget=TextInput(attrs=xlarge))

    prod_veg_per = forms.CharField(max_length=500,
                                   required=False,
                                   label=u"Production végétale perenne",
                                   widget=TextInput(attrs=large))

    prod_animal = forms.CharField(max_length=500,
                                  required=False,
                                  label=u"Production animale",
                                  widget=TextInput(attrs=large))

    class_ph = forms.ModelChoiceField(required=False,
                                      label=u"Classe PH",
                                      queryset=refs.ClassePH.objects.all().order_by('name'))

    class_prof = forms.ModelChoiceField(required=False,
                                        label=u"Classe Profondeur",
                                        queryset=refs.ClasseProfondeur.objects.all().order_by('name'))

    class_humid = forms.ModelChoiceField(required=False,
                                        label=u"Classe humidité",
                                        queryset=refs.ClasseHumidity.objects.all().order_by('name'))


    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-lg-2'
    helper.field_class = 'col-lg-10'
    helper.layout = layout.Layout(
        layout.Field('parcel'),
        layout.Field('name'),
        layout.Field('projets'),
        layout.Field('prod_veg_an'),
        layout.Field('prod_veg_per'),
        layout.Field('prod_animal'),
        layout.Field('class_ph'),
        layout.Field('class_prof'),
        layout.Field('class_humid'),        

        FormActions(
            layout.Submit('save_changes', 'Enregistrer', css_class="btn-primary"),
            layout.Submit('cancel', 'Annuler', css_class="btn-danger"),
            )
        )


class ParcelForm(forms.ModelForm):
    """
    Use to edit a Parcel
    """
    class Meta(object):
        model = models.Parcel
        # user will be set in views.ResumeNew
        # other fields will be set as model default
        exclude = ('nb_block', 'variables', 'center', 'polygon')

    name = forms.CharField(max_length=50,
                           required=True,
                           label=u"Name",
                           widget=TextInput(attrs=xlarge))



    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-lg-2'
    helper.field_class = 'col-lg-10'
    helper.layout = layout.Layout(
        layout.Field('name'),

        FormActions(
            layout.Submit('save_changes', 'Enregistrer', css_class="btn-primary"),
            layout.Submit('cancel', 'Annuler', css_class="btn-danger"),
            )
        )
