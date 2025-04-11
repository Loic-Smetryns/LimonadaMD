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

# third-party

from collections import defaultdict

from django.urls import reverse
from rest_framework.serializers import (HyperlinkedModelSerializer, SlugRelatedField, SerializerMethodField,
                                        IntegerField, CharField)

from .models import Membrane, MembraneTopol, MembraneTag, TopolComposition
from lipids.models import Lipid, Topology
from forcefields.models import Forcefield
from homepage.serializers import ReferenceSerializer

class ForcefieldSerializer(HyperlinkedModelSerializer):
    """
    Serializer for the Forcefield model, converting instances to JSON representations.
    Provides detailed information about force fields used in membrane simulations.

    Fields:
    - **name**: The name of the force field.
    - **details**: URL to access detailed information about the force field.

    Methods:
    - **get_details(forcefield)**: Generates an absolute URL for accessing detailed information about the force field.

    Meta:
    - **model**: The model associated with this serializer (Forcefield).
    - **fields**: List of fields to include in the JSON representation (name, details).
    """
    
    details = SerializerMethodField(read_only=True)
    
    class Meta:
        model = Forcefield
        fields = [ 'name', 'details' ]
        
    def get_details(self, forcefield):
        request = self.context.get('request')
        url = reverse('ffdetail', kwargs={'pk': forcefield.id})
        
        return request.build_absolute_uri(url) if request is not None else url

class MemListSerializer(HyperlinkedModelSerializer):
    """
    Serializer for the MembraneTopol model, converting instances to JSON representations.
    Includes custom fields and relationships to provide comprehensive membrane information.

    Fields:
    - details: URL to membrane details.
    - tags: List of tags associated with the membrane.
    - lipid_count: Total number of lipids in the membrane.
    - forcefield: Detailed information about the force field used for the membrane.
    - membrane_file: URL to the membrane file.
    - composition_file: URL to the composition file of the membrane.

    Methods:
    - get_details(membrane): Returns the absolute URL for membrane details.
    - get_forcefield_details(membrane): Returns the absolute URL for force field details.
    - get_membrane_file(membrane): Returns the absolute URL for the membrane file.
    - get_composition_file(membrane): Returns the absolute URL for the composition file.

    Meta:
    - model: Associated model (MembraneTopol).
    - fields: List of fields to include in the JSON representation.
    """
    
    details = SerializerMethodField(read_only=True)
    tags = SlugRelatedField(many=True, read_only=True, slug_field='tag')
    lipid_count = IntegerField(read_only=True, source='nb_lipids')
    forcefield = ForcefieldSerializer(read_only=True)
    membrane_file = SerializerMethodField(read_only=True)
    composition_file = SerializerMethodField(read_only=True)
    
    class Meta:
        model = MembraneTopol
        fields = [ 'details', 'name', 'tags', 'lipid_species_count', 'lipid_count', 'forcefield', 'membrane_file', 'composition_file' ]
        
    def get_details(self, membrane):
        request = self.context.get('request')
        url = reverse('api-memdetail', kwargs={'pk': membrane.id})
        
        return request.build_absolute_uri(url) if request is not None else url
    
    def get_membrane_file(self, membrane):
        request = self.context.get('request')
        file = membrane.mem_file
        
        #check if file is null
        if file.name == "":
            return ""
        
        return request.build_absolute_uri(file.url) if request is not None else file.url
    
    def get_composition_file(self, membrane):
        request = self.context.get('request')
        file = membrane.compo_file
        
        #check if file is null
        if file.name == "":
            return ""
        
        return request.build_absolute_uri(file.url) if request is not None else file.url

class LipidSerializer(HyperlinkedModelSerializer):
    """
    Serializer for the Lipid model, providing a JSON representation of lipid details.

    Fields:
    - name: Name of the lipid.
    - details: URL to detailed information about the lipid.

    Methods:
    - get_details(lipid): Returns the absolute URL for lipid details.

    Meta:
    - model: Associated model (Lipid).
    - fields: List of fields to include in the JSON representation.
    """
    
    details = SerializerMethodField()
    
    class Meta:
        model = Lipid
        fields = [ 'name', 'details' ]
        
    def get_details(self, lipid):
        request = self.context.get('request')
        url = reverse('api-lipdetail', kwargs={'slug': lipid.slug})
        
        return request.build_absolute_uri(url) if request is not None else url
    
class TopologySerializer(HyperlinkedModelSerializer):
    """
    Serializer for the Topology model, providing a JSON representation of topology details.

    Fields:
    - version: Version of the topology.
    - details: URL to detailed information about the topology.

    Methods:
    - get_details(topology): Returns the absolute URL for topology details.

    Meta:
    - model: Associated model (Topology).
    - fields: List of fields to include in the JSON representation.
    """
    
    details = SerializerMethodField()
    
    class Meta:
        model = Topology
        fields = [ 'version', 'details' ]
        
    def get_details(self, topology):
        request = self.context.get('request')
        url = reverse('api-topdetail', kwargs={'pk': topology.id})
        
        return request.build_absolute_uri(url) if request is not None else url

class TopolCompositionSerializer(HyperlinkedModelSerializer):
    """
    Serializer for the TopolComposition model, providing a JSON representation of topology composition details.

    Fields:
    - count: Number of lipids in the composition.
    - proportion: Proportion of lipids in the composition.
    - lipid: Detailed information about the lipid.
    - topology: Detailed information about the topology.

    Methods:
    - get_proportion(topol): Calculates the proportion of lipids in the composition.

    Meta:
    - model: Associated model (TopolComposition).
    - fields: List of fields to include in the JSON representation.
    """
    
    count = IntegerField(read_only=True, source='number')
    proportion = SerializerMethodField(read_only=True)
    lipid = LipidSerializer(read_only=True)
    topology = TopologySerializer(read_only=True)
    
    class Meta:
        model = TopolComposition
        fields = [ 'count', 'proportion', 'lipid', 'topology' ]
        
    def get_proportion(self, topol):
        total_number = self.context.get('total_number')
        return round(topol.number*100/total_number, 1) if total_number != None and total_number != 0 else 0.0
        

class MemDetailSerializer(HyperlinkedModelSerializer):
    """
    Serializer for detailed representation of the MembraneTopol model, providing comprehensive membrane details in JSON format.

    Fields:
    - lipids: Detailed information about the lipids in the membrane.
    - forcefield: Detailed information about the force field used for the membrane.
    - software: Name and version of the software used for the membrane.
    - membrane_file: URL to the membrane file.
    - composition_file: URL to the composition file of the membrane.
    - parameters_and_other_files: URL to other parameter files related to the membrane.
    - simulation_files: URL to access simulation files for the membrane.
    - lipid_count: Total number of lipids in the membrane.
    - tags: List of tags associated with the membrane.
    - proteins: List of proteins associated with the membrane.
    - reference: References related to the membrane.
    - composition: Detailed composition of the membrane, including lipid proportions.

    Methods:
    - get_lipids(membrane): Returns detailed information about the lipids in the membrane.
    - get_software(membrane): Returns the name and version of the software used for the membrane.
    - get_forcefield_details(membrane): Returns the absolute URL for force field details.
    - get_membrane_file(membrane): Returns the absolute URL for the membrane file.
    - get_composition_file(membrane): Returns the absolute URL for the composition file.
    - get_parameters_and_other_files(membrane): Returns the absolute URL for other parameter files.
    - get_simulation_files(membrane): Returns the absolute URL to access simulation files.
    - get_composition(membrane): Returns the detailed composition of the membrane, including lipid proportions.

    Meta:
    - model: Associated model (MembraneTopol).
    - fields: List of fields to include in the JSON representation.
    """
    
    lipids = SerializerMethodField(read_only=True)
    
    forcefield = ForcefieldSerializer(read_only=True)
    software = SerializerMethodField(read_only=True)
    membrane_file = SerializerMethodField(read_only=True)
    composition_file = SerializerMethodField(read_only=True)
    parameters_and_other_files = SerializerMethodField(read_only=True)
    simulation_files = SerializerMethodField(read_only=True)
    lipid_count = IntegerField(read_only=True, source='nb_lipids')
    tags = SlugRelatedField(many=True, read_only=True, slug_field='tag')
    proteins = SlugRelatedField(many=True, read_only=True, slug_field='prot', source='prot')
    reference = ReferenceSerializer(many=True, read_only=True)
    composition = SerializerMethodField(read_only=True)
    
    class Meta:
        model = MembraneTopol
        fields=[ 
            'name', 'lipid_species_count', 'lipids', 'forcefield', 'software', 'membrane_file', 'composition_file',
            'parameters_and_other_files', 'simulation_files', 'lipid_count', 'temperature', 'equilibration', 'tags', 'proteins',
            'description', 'reference', 'composition'
        ]
    
    def get_lipids(self, membrane):
        compositions = membrane.topolcomposition_set.select_related('lipid', 'topology').all()
        unique_lipids = {comp.lipid for comp in compositions if comp.lipid}
        return LipidSerializer(unique_lipids, many=True, context=self.context).data
    
    def get_software(self, membrane):
        return membrane.software.name + ' ' + membrane.software.version
    
    def get_membrane_file(self, membrane):
        request = self.context.get('request')
        file = membrane.mem_file
        
        if file.name == "":
            return ""
        
        return request.build_absolute_uri(file.url) if request is not None else file.url
    
    def get_composition_file(self, membrane):
        request = self.context.get('request')
        file = membrane.compo_file
        
        if file.name == "":
            return ""
        
        return request.build_absolute_uri(file.url) if request is not None else file.url
    
    def get_parameters_and_other_files(self, membrane):
        request = self.context.get('request')
        file = membrane.other_file
        
        return request.build_absolute_uri(file.url) if request is not None else file.url
    
    def get_simulation_files(self, membrane):
        request = self.context.get('request')
        url = reverse('getfiles') + f'?memid={membrane.id}'
        
        return request.build_absolute_uri(url) if request is not None else url
    
    def get_composition(self, membrane):
        topol_composition = membrane.topolcomposition_set.all().order_by('-number')
        
        composition = defaultdict(list)
        total_numbers = defaultdict(int)
        
        for topol_c in topol_composition:
            total_numbers[topol_c.side] += topol_c.number
        
        format_side = lambda x: x.replace('LO', 'lower_leaflet').replace('UP', 'upper_leaflet')
        for topol_c in topol_composition:
            composition[format_side(topol_c.side)].append(
                TopolCompositionSerializer(topol_c, context={**self.context, 'total_number': total_numbers[topol_c.side]}).data
            )
        
        
        return composition