from rest_framework import serializers
from .models import *


class CourseSerializer(serializers.Serializer):
    class Meta:
        model = Course
        fields = ['name', 'description', 'created_by', 'last_update',
                  'requirements', 'objectives', 'price',
                  'category', 'welcome_message']
