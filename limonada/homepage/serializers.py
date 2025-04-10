from django.urls import reverse
from rest_framework.serializers import (HyperlinkedModelSerializer, SlugRelatedField, SerializerMethodField,
                                        IntegerField, CharField)

from .models import Reference

class ReferenceSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Reference
        fields = [ 'doi', 'title', 'journal', 'year', 'date', 'volume', 'refid' ]