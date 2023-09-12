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
        fields = ['rating', 'body']


class CoreUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'first_name', 'last_name', 'email']


class MainUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = CoreUserSerializer()

    class Meta:
        model = User
        fields = ['id', 'user', 'rating', 'bio']


class EnrollmentUserPrespectiveSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Enrollment
        fields = ['id', 'user']


class EnrollmentCoursePrespectiveSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    course = CourseSerializer()

    class Meta:
        model = Enrollment
        fields = ['id', 'course']
