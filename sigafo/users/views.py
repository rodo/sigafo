# -*- coding: utf-8 -*-  pylint: disable-msg=R0801
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
import logging
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from sigafo.projet.models import Projet
from sigafo.parc.models import Parcel, Site

logger = logging.getLogger(__name__)


@login_required
def profile(request):
    """The home page
    """
    projets = Projet.objects.filter(users__in=[request.user.id])    

    
    nb_parcel = Parcel.objects.all().count()
    nb_site = Site.objects.all().count()


    return render(request,
                  'profile.html',
                  {'my_projects': projets,
                   'user': request.user,
                   'nb_parcel': nb_parcel,
                   'nb_site': nb_site})
