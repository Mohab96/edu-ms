from rest_framework import serializers
from .models import *


class CourseSerializer(serializers.ModelSerializer):
    # reviews_count = serializers.SerializerMethodField(method_name='reviews_count')
    # students_count = serializers.SerializerMethodField(method_name='students_count')

    # def reviews_count(self, course):
    #     return Review.objects.filter(course__id=course.id).count()

    # def students_count(self, course):
    #     return Student.objects.filter(courses__id=course.id).count()

    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'created_by', 'last_update',
                  'requirements', 'objectives', 'price',
                  'category', 'welcome_message']#, 'reviews_count', 'students_count']