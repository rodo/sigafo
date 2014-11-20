============
Référentiels
============

.. toctree::
   :maxdepth: 2

Système de production
---------------------
class SystemProd(models.Model):

Production animale
------------------
class AnimalProduction(models.Model):

Production végétale annuelle
----------------------------
class VegetalProductionAnnual(models.Model):

Production végétele pérenne
---------------------------
class VegetalProductionPerennial(models.Model):

Façon culturale
---------------
class Tillage(models.Model):

Topographie
-----------
class Topography(models.Model):

Texture
-------
class Texture(models.Model):

Exemples

* Limoneuse
* Sableuse
* Argilo-limoneuse

Classe de PH
------------
class ClassePH(models.Model):

Classe de profondeur
--------------------
class ClasseProfondeur(models.Model):

Classe d'humidité
-----------------
class ClasseHumidity(models.Model):

Thèmes expérimentaux
--------------------

Définit les thèmes expérimentaux présents sur une `parcelle`

class ExperimentalSubjects(models.Model):


Nature de bloc
--------------

Classe de modélisation `class NatureBlock(models.Model):`

Éléments paysagers environnants
-------------------------------

Nom de la classe de modélisation technique `class
ElmtsPaysage(models.Model):`

Exemples de valeurs

* Bosquets 
* Haies  
* Murets
* Mare
* Rivière
* Route
