# -*- coding: utf-8; Mode: python; tab-width: 4; indent-tabs-mode:nil; -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
#
#    Limonada is accessible at https://limonada.univ-reims.fr/
#    Copyright (C) 2016-2020 - The Limonada Team (see the AUTHORS file)
#
#    This file is part of Limonada.
#
#    Limonada is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Limonada is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Limonada.  If not, see <http://www.gnu.org/licenses/>.

# Django
from django import template

register = template.Library()


@register.simple_tag
def lipidnames(qs):
    """ This function makes a list of lipid species in the composition.
    """
    return list({comp.lipid for comp in qs.select_related('lipid')})


@register.simple_tag()
def side_select(nbmemb):
    """
    """
    UPPER = 'UP'
    LOWER = 'LO'
    LEAFLET_CHOICES = ((UPPER, 'Upper leaflet'),
                       (LOWER, 'Lower leaflet'))
    if nbmemb > 0:
        for i in range(nbmemb):
            LEAFLET_CHOICES += (('UP%d' % (i+2), 'Upper leaflet %d' % (i+2)),
                                ('LO%d' % (i+2), 'Lower leaflet %d' % (i+2)))
    LEAFLET_CHOICES += ((('UNK', 'Not in leaflet')),)

    return LEAFLET_CHOICES


@register.filter(name='times')
def times(number):

    return range(number)


@register.simple_tag
def boolean(val=None):
    return 1 if val == 0 else 0


@register.filter(name='hash')
def hash(h, key):
    return h[key]


@register.simple_tag()
def get_percent(nb_lip_per_leaflet, leaflet, nb):
    percent = "%5.1f" % (100 * float(nb) / float(nb_lip_per_leaflet[leaflet]))

    return percent
