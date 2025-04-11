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

from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework import status

from membranes.models import MembraneTopol, Membrane, MembraneTag
from forcefields.models import Forcefield, Software

class ManyNullFieldAPIMemListTestCase(APITestCase):
    
    def setUp(self):
        user = User.objects.create(
            username='intern', first_name='Loïc', last_name='Smetryns', email='loic.smetryns@gmail.com',
            password='Oh no, the intern left another Easter egg in the code...'
        )
        
        forcefield = Forcefield.objects.create(curator = user)
        
        software = Software.objects.create()
        
        MembraneTopol.objects.create(
            id=1, name='mammalian plasma membrane', temperature=310, equilibration=10000, curator=user, forcefield=forcefield,
            software=software
        )
        
        MembraneTopol.objects.create(
            id=2, name='yeast pm1', temperature=303, equilibration=200, curator=user, forcefield=forcefield,
            software=software
        )
        
    def tearDown(self):
        User.objects.all().delete()
        Forcefield.objects.all().delete()
        Software.objects.all().delete()
        MembraneTopol.objects.all().delete()

    def test_membrane_list(self):
        url = reverse('api-memlist')
        response = self.client.get(url)
        
        # check the status_code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # check json structure
        self.assertEqual(len(response.data), 4)
        self.assertTrue('count' in response.data.keys())
        self.assertTrue('next' in response.data.keys())
        self.assertTrue('previous' in response.data.keys())
        self.assertTrue('results' in response.data.keys())
        
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(len(response.data['results']), 2)
        
        # check if names are valids 
        names = tuple(map(lambda x: x['name'], response.data['results']))
        
        self.assertTrue('mammalian plasma membrane' in names)
        self.assertTrue('yeast pm1' in names)
        
        # check other fields
        m1=None
        m2=None
        
        m1=response.data['results'][0]
        m2=response.data['results'][1]
        
        if m1['name'] == 'yeast pm1':
            m1, m2 = m2, m1
        
        self.assertEqual(m1['details'], 'http://testserver/membranes/api/v1/1/')
        self.assertEqual(m1['membrane_file'], '')
        self.assertEqual(m1['composition_file'], '')
        self.assertEqual(m1['tags'], [])
        self.assertEqual(m1['lipid_species_count'], 0)
        self.assertEqual(m1['lipid_count'], 0)
        self.assertEqual(m1['forcefield']['name'], '')
        
        self.assertEqual(m2['details'], 'http://testserver/membranes/api/v1/2/')
        self.assertEqual(m2['membrane_file'], '')
        self.assertEqual(m2['composition_file'], '')
        self.assertEqual(m2['tags'], [])
        self.assertEqual(m2['lipid_species_count'], 0)
        self.assertEqual(m2['lipid_count'], 0)
        self.assertEqual(m2['forcefield']['name'], '')
        
class FilledFieldAPIMemListTestCase(APITestCase):
    
    def setUp(self):
        user = User.objects.create(
            username='intern', first_name='Loïc', last_name='Smetryns', email='loic.smetryns@gmail.com',
            password='Oh no, the intern left another Easter egg in the code...'
        )
        
        forcefield = Forcefield.objects.create(id=1, curator = user, name='martini 2.0')
        
        software = Software.objects.create()
        
        membrane = Membrane.objects.create(nb_liptypes=63)
        
        tag1 = MembraneTag.objects.create(tag='mammalian')
        tag2 = MembraneTag.objects.create(tag='plasma membrane')
        
        membrane.tag.add(tag1, tag2)
        
        MembraneTopol.objects.create(
            id=1, name='mammalian plasma membrane', temperature=310, equilibration=10000, curator=user, forcefield=forcefield,
            software=software, membrane=membrane, nb_lipids=6664, compo_file="membranes/LIM1_mammalian_plasma_membrane.txt",
            mem_file='membranes/LIM1_mammalian_plasma_membrane.gro'
        )
        
    def tearDown(self):
        User.objects.all().delete()
        Forcefield.objects.all().delete()
        Software.objects.all().delete()
        MembraneTopol.objects.all().delete()

    def test_membrane_list(self):
        url = reverse('api-memlist')
        response = self.client.get(url)
        
        # check the status_code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # check json structure
        self.assertEqual(len(response.data), 4)
        self.assertTrue('count' in response.data.keys())
        self.assertTrue('next' in response.data.keys())
        self.assertTrue('previous' in response.data.keys())
        self.assertTrue('results' in response.data.keys())
        
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(len(response.data['results']), 1)
        
        # check fields
        m = response.data['results'][0]
        
        self.assertEqual(m['name'], 'mammalian plasma membrane')
        self.assertEqual(m['details'], 'http://testserver/membranes/api/v1/1/')
        
        self.assertEqual(len(m['tags']), 2)
        self.assertTrue('mammalian' in m['tags'])
        self.assertTrue('plasma membrane' in m['tags'])
        
        self.assertEqual(m['lipid_species_count'], 63)
        self.assertEqual(m['lipid_count'], 6664)
        
        self.assertEqual(m['forcefield']['name'], 'martini 2.0')
        self.assertEqual(m['forcefield']['details'], 'http://testserver/forcefields/1/')
        
        self.assertEqual(m['membrane_file'], "http://testserver/media/membranes/LIM1_mammalian_plasma_membrane.gro")
        self.assertEqual(m['composition_file'], "http://testserver/media/membranes/LIM1_mammalian_plasma_membrane.txt")
        
        