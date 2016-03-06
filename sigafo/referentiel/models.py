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
# App : referentiel
#
from django.db import models
from uuidfield import UUIDField

class refModel(models.Model):

    uuid = UUIDField(auto=True)
    name = models.CharField(max_length=300)
    comment = models.TextField(blank=True, null=True)
    # technical field
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        """The unicode method
        """
        return "%s" % (self.name)

class SystemProd(refModel):
    """Systeme de production agroforestier
    """

class AnimalProduction(refModel):
    """Systeme de production agroforestier
    """

class VegetalProductionAnnual(refModel):
    """Systeme de production agroforestier
    """


class VegetalProductionPerennial(refModel):
    """Systeme de production agroforestier
    """

class Tillage(refModel):
    """Façon culturales
    """

class Fertilisation(refModel):
    """Fertilisation
    """


class TraitPhyto(refModel):
    """Traitement phytosanitaire
    """


class ModeConduite(refModel):
    """Mode de consuite des blocs
    """


class Topography(refModel):
    """Systeme de production agroforestier
    """

class Texture(refModel):
    """
    """

class ExperimentalDevice(refModel):
    """
    """


class ClassePH(refModel):
    """
    Classe de PU
    """


class ClasseProfondeur(refModel):
    """
    Classe de profondeur
    """


class ClasseHumidity(refModel):
    """
    """


class ExperimentalSubjects(refModel):
    """Thèmes experimentaux
    """


class NatureBlock(refModel):
    """Nature du bloc
    """


class ElmtsPaysage(refModel):
    """Elèments paysagers environnants
    """

class AmNature(refModel):
    """ Aménagements

    Nature de l'aménagement
    """

class AmObjectifInit(refModel):
    """ Aménagements

    Objectif de l'aménagement
    """

class AmEssence(refModel):
    """ Aménagements

    Essence de l'aménagement
    """


class AmConduite(refModel):
    """ Aménagements

    Conduite de l'aménagement
    """


class AmProtection(refModel):
    """ Aménagements

    Protection de l'aménagement
    """


class AmPaillage(refModel):
    """ Aménagements

    Paillage de l'aménagement
    """

class AmGestionbe(refModel):
    """ Aménagements

    Gestion de la bande enherbée
    """

class AmNaturebe(refModel):
    """ Aménagements

    Nature de la bande enherbée

    """
