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


class SystemProd(models.Model):
    """Systeme de production agroforestier
    """
    uuid = UUIDField(auto=True)    
    name = models.CharField(max_length=300)
    comment = models.TextField(blank=True)

    def __unicode__(self):
        """The unicode method
        """
        return "%s" % (self.name)


class AnimalProduction(models.Model):
    """Systeme de production agroforestier
    """
    uuid = UUIDField(auto=True)
    name = models.CharField(max_length=300)
    comment = models.TextField(blank=True)

    def __unicode__(self):
        """The unicode method
        """
        return "%s" % (self.name)


class VegetalProductionAnnual(models.Model):
    """Systeme de production agroforestier
    """
    uuid = UUIDField(auto=True)
    name = models.CharField(max_length=300)
    comment = models.TextField(blank=True)

    def __unicode__(self):
        """The unicode method
        """
        return "%s" % (self.name)


class VegetalProductionPerennial(models.Model):
    """Systeme de production agroforestier
    """
    uuid = UUIDField(auto=True)
    name = models.CharField(max_length=300)
    comment = models.TextField(blank=True)

    def __unicode__(self):
        """The unicode method
        """
        return "%s" % (self.name)


class Tillage(models.Model):
    """Façon culturales
    """
    uuid = UUIDField(auto=True)
    name = models.CharField(max_length=300)
    comment = models.TextField(blank=True)

    def __unicode__(self):
        """The unicode method
        """
        return "%s" % (self.name)


class Fertilisation(models.Model):
    """Fertilisation
    """
    uuid = UUIDField(auto=True)
    name = models.CharField(max_length=300)
    comment = models.TextField(blank=True)

    def __unicode__(self):
        """The unicode method
        """
        return "%s" % (self.name)


class TraitPhyto(models.Model):
    """Traitement phytosanitaire
    """
    uuid = UUIDField(auto=True)
    name = models.CharField(max_length=300)
    comment = models.TextField(blank=True)

    def __unicode__(self):
        """The unicode method
        """
        return "%s" % (self.name)


class ModeConduite(models.Model):
    """Mode de consuite des blocs
    """
    uuid = UUIDField(auto=True)
    name = models.CharField(max_length=300)
    comment = models.TextField(blank=True)

    def __unicode__(self):
        """The unicode method
        """
        return "%s" % (self.name)


class Topography(models.Model):
    """Systeme de production agroforestier
    """
    uuid = UUIDField(auto=True)
    name = models.CharField(max_length=300)
    comment = models.TextField(blank=True)

    def __unicode__(self):
        """The unicode method
        """
        return "%s" % (self.name)


class Texture(models.Model):
    """
    """
    uuid = UUIDField(auto=True)
    name = models.CharField(max_length=300)
    comment = models.TextField(blank=True)

    def __unicode__(self):
        """The unicode method
        """
        return "%s" % (self.name)


class ExperimentalDevice(models.Model):
    """
    """
    uuid = UUIDField(auto=True)
    name = models.CharField(max_length=300)
    comment = models.TextField(blank=True)

    def __unicode__(self):
        """The unicode method
        """
        return "%s" % (self.name)


class ClassePH(models.Model):
    """
    """
    uuid = UUIDField(auto=True)
    name = models.CharField(max_length=300)
    comment = models.TextField(blank=True)

    def __unicode__(self):
        """The unicode method
        """
        return "%s" % (self.name)


class ClasseProfondeur(models.Model):
    """
    """
    uuid = UUIDField(auto=True)
    name = models.CharField(max_length=300)
    comment = models.TextField(blank=True)

    def __unicode__(self):
        """The unicode method
        """
        return "%s" % (self.name)


class ClasseHumidity(models.Model):
    """
    """
    uuid = UUIDField(auto=True)
    name = models.CharField(max_length=300)
    comment = models.TextField(blank=True)

    def __unicode__(self):
        """The unicode method
        """
        return "%s" % (self.name)


class ExperimentalSubjects(models.Model):
    """Thèmes experimentaux
    """
    uuid = UUIDField(auto=True)
    name = models.CharField(max_length=300)
    comment = models.TextField(blank=True)

    def __unicode__(self):
        """The unicode method
        """
        return "%s" % (self.name)


class NatureBlock(models.Model):
    """Nature du bloc
    """
    uuid = UUIDField(auto=True)
    name = models.CharField(max_length=300)
    comment = models.TextField(blank=True)

    def __unicode__(self):
        """The unicode method
        """
        return "%s" % (self.name)


class ElmtsPaysage(models.Model):
    """Elèments paysagers environnants
    """
    uuid = UUIDField(auto=True)
    name = models.CharField(max_length=300)
    comment = models.TextField(blank=True)

    def __unicode__(self):
        """The unicode method
        """
        return "%s" % (self.name)


class AmNature(models.Model):
    """ Aménagements

    Nature de l'aménagement
    """
    uuid = UUIDField(auto=True)    
    name = models.CharField(max_length=300)
    comment = models.TextField(blank=True)

    def __unicode__(self):
        """The unicode method
        """
        return "%s" % (self.name)


class AmObjectifInit(models.Model):
    """ Aménagements

    Objectif de l'aménagement
    """
    uuid = UUIDField(auto=True)    
    name = models.CharField(max_length=300)
    comment = models.TextField(blank=True)

    def __unicode__(self):
        """The unicode method
        """
        return "%s" % (self.name)

class AmEssence(models.Model):
    """ Aménagements

    Essence de l'aménagement
    """
    uuid = UUIDField(auto=True)    
    name = models.CharField(max_length=300)
    comment = models.TextField(blank=True)

    def __unicode__(self):
        """The unicode method
        """
        return "%s" % (self.name)


class AmConduite(models.Model):
    """ Aménagements

    Conduite de l'aménagement
    """
    uuid = UUIDField(auto=True)    
    name = models.CharField(max_length=300)
    comment = models.TextField(blank=True)

    def __unicode__(self):
        """The unicode method
        """
        return "%s" % (self.name)


class AmProtection(models.Model):
    """ Aménagements

    Protection de l'aménagement
    """
    uuid = UUIDField(auto=True)    
    name = models.CharField(max_length=300)
    comment = models.TextField(blank=True)

    def __unicode__(self):
        """The unicode method
        """
        return "%s" % (self.name)


class AmPaillage(models.Model):
    """ Aménagements

    Paillage de l'aménagement
    """
    uuid = UUIDField(auto=True)    
    name = models.CharField(max_length=300)
    comment = models.TextField(blank=True)

    def __unicode__(self):
        """The unicode method
        """
        return "%s" % (self.name)


class AmGestionbe(models.Model):
    """ Aménagements

    Gestion de la bande enherbée
    """
    uuid = UUIDField(auto=True)    
    name = models.CharField(max_length=300)
    comment = models.TextField(blank=True)

    def __unicode__(self):
        """The unicode method
        """
        return "%s" % (self.name)

class AmNaturebe(models.Model):
    """ Aménagements

    Nature de la bande enherbée

    """
    uuid = UUIDField(auto=True)    
    name = models.CharField(max_length=300)
    comment = models.TextField(blank=True)

    def __unicode__(self):
        """The unicode method
        """
        return "%s" % (self.name)
