from django.urls import reverse
from rest_framework.serializers import (HyperlinkedModelSerializer, SlugRelatedField, SerializerMethodField,
                                        IntegerField, CharField)

from .models import Membrane, MembraneTopol, MembraneTag
from lipids.models import Lipid
from homepage.serializers import ReferenceSerializer

class MemListSerializer(HyperlinkedModelSerializer):
    """
    Serializer for the MembraneTopol model, converting instances to JSON representations.
    Includes custom fields and relationships to provide comprehensive membrane information.

    Fields:
    - details: URL to membrane details.
    - tags: List of tags associated with the membrane.
    - lipid_species: Number of lipid types in the membrane.
    - lipids: Total number of lipids in the membrane.
    - forcefield: Name of the force field used for the membrane.
    - membrane_file: URL to the membrane file.
    - composition_file: URL to the composition file of the membrane.

    Methods:
    - get_details(membrane): Returns the absolute URL for membrane details.
    - get_membrane_file(membrane): Returns the absolute URL for the membrane file.
    - get_composition_file(membrane): Returns the absolute URL for the composition file.

    Meta:
    - model: Associated model (MembraneTopol).
    - fields: List of fields to include in the JSON representation.
    """
    
    details = SerializerMethodField(read_only=True)
    tags = SlugRelatedField(many=True, read_only=True, slug_field='tag', source='membrane.tag')
    lipid_species = SlugRelatedField(read_only=True, slug_field='nb_liptypes', source='membrane')
    lipids = IntegerField(read_only=True, source='nb_lipids')
    forcefield = SlugRelatedField(read_only=True, slug_field='name')
    forcefield_details = SerializerMethodField(read_only=True)
    membrane_file = SerializerMethodField(read_only=True)
    composition_file = SerializerMethodField(read_only=True)
    
    class Meta:
        model = MembraneTopol
        fields = [ 'details', 'name', 'tags', 'lipid_species', 'lipids', 'forcefield', 'forcefield_details', 'membrane_file', 'composition_file' ]
        
    def get_details(self, membrane):
        request = self.context.get('request')
        url = reverse('api-memdetail', kwargs={'pk': membrane.id})
        
        return request.build_absolute_uri(url) if request is not None else url
    
    def get_forcefield_details(self, membrane):
        request = self.context.get('request')
        url = reverse('ffdetail', kwargs={'pk': membrane.forcefield.id})
        
        return request.build_absolute_uri(url) if request is not None else url
    
    def get_membrane_file(self, membrane):
        request = self.context.get('request')
        file = membrane.mem_file
        
        return request.build_absolute_uri(file.url) if request is not None else file.url
    
    def get_composition_file(self, membrane):
        request = self.context.get('request')
        file = membrane.compo_file
        
        return request.build_absolute_uri(file.url) if request is not None else file.url

class LipidSerializer(HyperlinkedModelSerializer):
    details = SerializerMethodField()
    
    class Meta:
        model = Lipid
        fields = [ 'name', 'details' ]
        
    def get_details(self, lipid):
        request = self.context.get('request')
        url = reverse('api-lipdetail', kwargs={'slug': lipid.slug})
        
        return request.build_absolute_uri(url) if request is not None else url

class MemDetailSerializer(HyperlinkedModelSerializer):
    lipid_species = SlugRelatedField(read_only=True, slug_field='nb_liptypes', source='membrane')
    
    lipids = SerializerMethodField(read_only=True)
    
    forcefield = SlugRelatedField(read_only=True, slug_field='name')
    forcefield_details = SerializerMethodField(read_only=True)
    software = SerializerMethodField(read_only=True)
    membrane_file = SerializerMethodField(read_only=True)
    composition_file = SerializerMethodField(read_only=True)
    parameters_and_other_files = SerializerMethodField(read_only=True)
    simulation_files = SerializerMethodField(read_only=True)
    lipids_number = IntegerField(read_only=True, source='nb_lipids')
    tags = SlugRelatedField(many=True, read_only=True, slug_field='tag', source='membrane.tag')
    proteins = SlugRelatedField(many=True, read_only=True, slug_field='prot', source='prot')
    reference = ReferenceSerializer(many=True, read_only=True)
    
    class Meta:
        model = MembraneTopol
        fields=[ 
            'name', 'lipid_species', 'lipids', 'forcefield', 'forcefield_details', 'software', 'membrane_file', 'composition_file',
            'parameters_and_other_files', 'simulation_files', 'lipids_number', 'temperature', 'equilibration', 'tags', 'proteins',
            'description', 'reference'
        ]
    
    def get_lipids(self, membrane):
        compositions = membrane.topolcomposition_set.select_related('lipid', 'topology').all()
        unique_lipids = {comp.lipid for comp in compositions if comp.lipid}
        return LipidSerializer(unique_lipids, many=True).data
    
    def get_software(self, membrane):
        return membrane.software.name + ' ' + membrane.software.version
    
    def get_forcefield_details(self, membrane):
        request = self.context.get('request')
        url = reverse('ffdetail', kwargs={'pk': membrane.forcefield.id})
        
        return request.build_absolute_uri(url) if request is not None else url
    
    def get_membrane_file(self, membrane):
        request = self.context.get('request')
        file = membrane.mem_file
        
        return request.build_absolute_uri(file.url) if request is not None else file.url
    
    def get_composition_file(self, membrane):
        request = self.context.get('request')
        file = membrane.compo_file
        
        return request.build_absolute_uri(file.url) if request is not None else file.url
    
    def get_parameters_and_other_files(self, membrane):
        request = self.context.get('request')
        file = membrane.other_file
        
        return request.build_absolute_uri(file.url) if request is not None else file.url
    
    def get_simulation_files(self, membrane):
        request = self.context.get('request')
        url = reverse('getfiles') + f'?memid={membrane.id}'
        
        return request.build_absolute_uri(url) if request is not None else url
        