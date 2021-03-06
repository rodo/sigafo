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
"""
Fulltext indexing with haystack
"""
from haystack import indexes
from sigafo.parc.models import Site, Parcel, Block, Observation


class BlockIndex(indexes.SearchIndex, indexes.Indexable):
    """
    Fulltext indexing for objects Block
    """
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')

    def get_model(self):
        return Block

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


class SiteIndex(indexes.SearchIndex, indexes.Indexable):
    """
    Fulltext indexing for objects Site
    """
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')

    def get_model(self):
        return Site

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


class ParcelIndex(indexes.SearchIndex, indexes.Indexable):
    """
    Fulltext indexing for objects Parcel
    """
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')

    def get_model(self):
        return Parcel

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


class ObservationIndex(indexes.SearchIndex, indexes.Indexable):
    """
    Fulltext indexing for objects Observation
    """
    text = indexes.CharField(document=True, use_template=True)
    observation = indexes.CharField(model_attr='observation')
    comment = indexes.CharField(model_attr='comment')

    def get_model(self):
        return Observation

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
