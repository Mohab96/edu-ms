from rest_framework import serializers
from .models import *
from core.models import CoreUser
from django.db import transaction


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


class ReviewCoursePrespectiveSerializer(serializers.ModelSerializer):
    def get_course_id(self, review):
        return self.context['course_id']

    class Meta:
        model = Review
        fields = ['id', 'course_id', 'student', 'rating', 'body']

    def create(self, validated_data):
        course_id = self.context['course_id']
        return Review.objects.create(course_id=course_id, **validated_data)


class ReviewUpdateCoursePrespectiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['rating', 'body']


class GeneralReviewSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'course', 'student', 'rating', 'body']


class GeneralCoreUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(read_only=True)

    class Meta:
        model = CoreUser
        fields = ['id', 'username', 'email', 'first_name',
                  'last_name', 'password']


class GeneralMainUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    rating = serializers.DecimalField(
        read_only=True, max_digits=3, decimal_places=1)
    core_user = GeneralCoreUserSerializer()
    # created_by = CourseSerializer(many=True, read_only=True)
    # enrolled_in = CourseSerializer(many=True, read_only=True)

    def update(self, instance, validated_data):
        with transaction.atomic():
            instance.bio = validated_data.get('bio', instance.bio)
            instance.core_user.first_name = validated_data.get(
                'core_user').get('first_name', instance.core_user.first_name)
            instance.core_user.last_name = validated_data.get(
                'core_user').get('last_name', instance.core_user.last_name)
            instance.core_user.username = validated_data.get(
                'core_user').get('username', instance.core_user.username)
            instance.core_user.password = validated_data.get(
                'core_user').get('password', instance.core_user.password)

            instance.save()
            return instance

    class Meta:
        model = User
        fields = ['id', 'core_user', 'rating',
                  'bio']  # , 'created_by', 'enrolled_in']


class RegisterCoreUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoreUser
        fields = ['first_name', 'last_name', 'username', 'email', 'password']


class CreateMainUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    core_user = RegisterCoreUserSerializer()

    def create(self, validated_data):
        with transaction.atomic():
            _first_name = validated_data.get('core_user').get('first_name')
            _last_name = validated_data.get('core_user').get('last_name')
            _username = validated_data.get('core_user').get('username')
            _email = validated_data.get('core_user').get('email')
            _password = validated_data.get('core_user').get('password')

            core_user_instance = CoreUser.objects.create(
                first_name=_first_name,
                last_name=_last_name,
                username=_username,
                email=_email,
                password=_password
            )
            core_user_instance.save()

            instance = User.objects.create(core_user=core_user_instance)
            instance.save()
            return instance

    class Meta:
        model = User
        fields = ['id', 'core_user']


class EnrollmentCoursePrespectiveSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Enrollment
        fields = ['id', 'user']


class EnrollmentUserPrespectiveSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    course = CourseSerializer()

    class Meta:
        model = Enrollment
        fields = ['id', 'course']


class GeneralEnrollmentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Enrollment
        fields = ['id', 'course', 'user']


class GeneralCategorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    courses_count = serializers.SerializerMethodField(read_only=True)

    def get_courses_count(self, category):
        return Course.objects.filter(category__id=category.id).count()

    class Meta:
        model = Category
        fields = ['id', 'name', 'courses_count']
