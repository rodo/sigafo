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
from sigafo.contact.models import Contact


class ContactIndex(indexes.SearchIndex, indexes.Indexable):
    """
    Fulltext indexing for objects Contact
    """
    text = indexes.CharField(document=True, use_template=True)
    firstname = indexes.CharField(model_attr='firstname')
    lastname = indexes.CharField(model_attr='lastname')

    def get_model(self):
        return Contact

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
