from django.db import models
from django.contrib.gis.db import models
from django_hstore import hstore

# Create your models here.
class GeoHStoreManager(models.GeoManager, hstore.HStoreManager):
    pass
