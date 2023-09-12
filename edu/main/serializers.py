from rest_framework import serializers
from .models import *
from core import models


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'created_by', 'last_update',
                  'requirements', 'objectives', 'price', 'category',
                  'welcome_message']


class CourseUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['name', 'description', 'requirements', 'objectives',
                  'price', 'category', 'welcome_message']


class ReviewSerializer(serializers.ModelSerializer):
    def get_course_id(self, review):
        return self.context['course_id']

    class Meta:
        model = Review
        fields = ['id', 'course_id', 'student', 'rating', 'body']

    def create(self, validated_data):
        course_id = self.context['course_id']
        return Review.objects.create(course_id=course_id, **validated_data)


class ReviewUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['student', 'rating', 'body']
