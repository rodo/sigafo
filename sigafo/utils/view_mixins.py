# -*- coding: utf-8 -*-  pylint: disable-msg=R0801
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

"""
A set of usefull mixins usable in all the project
"""
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page


class ProtectedMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProtectedMixin, self).dispatch(*args, **kwargs)


class StaffOnlyMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(StaffOnlyMixin, self).dispatch(*args, **kwargs)


class DetailProtected(ProtectedMixin, DetailView):
    pass

class ListProtected(ProtectedMixin, ListView):
    pass


class APICacheMixin(object):
    cache_timeout = 300
    
    def get_cache_timeout(self):
        return self.cache_timeout

    def dispatch(self, *args, **kwargs):
        return cache_page(self.get_cache_timeout())(super(APICacheMixin, self).dispatch)(*args, **kwargs)
     

class APIPCacheMixin(ProtectedMixin):
    cache_timeout = 300
    
    def get_cache_timeout(self):
        return self.cache_timeout

    def dispatch(self, *args, **kwargs):
        return cache_page(self.get_cache_timeout())(super(APIPCacheMixin, self).dispatch)(*args, **kwargs)
     
