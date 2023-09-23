from rest_framework import serializers
from .models import *
from core.models import CoreUser
from django.db import transaction
# from rest_framework.response import Response
# from rest_framework import status
# from django.shortcuts import get_object_or_404


class MaterialItemSerializer(serializers.ModelSerializer):
    file = serializers.FileField()

    def create(self, validated_data):
        course_id = self.context['course_id']
        instance = MaterialItem.objects.create(
            course_id=course_id,
            **validated_data
        )

        return instance

    def update(self, instance, validated_data):
        with transaction.atomic():
            instance.name = validated_data.get('name', instance.name)
            instance.file = validated_data.get('file', instance.file)

        instance.save()
        return instance

    class Meta:
        model = MaterialItem
        fields = ['id', 'name', 'file']


class CourseSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    items = MaterialItemSerializer(many=True, read_only=True)

    def create(self, validated_data):
        instance = Course.objects.create(**validated_data)
        return instance

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'created_by', 'last_update',
                  'requirements', 'objectives', 'price', 'category',
                  'welcome_message', 'items']


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


class CartItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    student_id = serializers.SerializerMethodField(read_only=True)

    def get_student_id(self, cart_item):
        return Cart.objects.filter(id=self.context['cart_id'])[0].student_id

    class Meta:
        model = CartItem
        fields = ['id', 'student_id', 'course_id']


class CreateCartItemSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        print(validated_data)
        course_id = validated_data['course_id']
        condition = CartItem.objects.filter(cart_id=self.context['cart_id']) \
                                       .filter(course_id=course_id).exists()

        if condition:
            return CartItem.objects.get(cart_id=self.context['cart_id'],
                                    course_id=course_id)

        return CartItem.objects.create(cart_id=self.context['cart_id'],
                                    course_id=course_id)

    class Meta:
        model = CartItem
        fields = ['id', 'course_id', 'cart_id']
        read_only_fields = ('id', 'cart_id',)


class UpdateCartItemSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        print(instance.__dict__, validated_data)
        current_course_id = instance.course_id
        new_course_id = validated_data.get('course_id', instance.course_id)

        if current_course_id != new_course_id:
            condition = CartItem.objects\
                .filter(cart_id=instance.cart_id) \
                .filter(course_id=new_course_id) \
                .exists()

            if not condition:
                with transaction.atomic():
                    CartItem.objects \
                        .filter(id=instance.id) \
                        .update(course_id=new_course_id)
            else:
                CartItem.objects.filter(id=instance.id).delete()

        return CartItem.objects.filter(cart_id=instance.cart_id) \
            .filter(course_id=current_course_id)

    class Meta:
        model = CartItem
        fields = ['id', 'course_id']
        read_only_fields = ('id', )


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'student_id']


class GeneralCoreUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(read_only=True)
    username = serializers.CharField(max_length=150, read_only=True)

    class Meta:
        model = CoreUser
        fields = ['id', 'username', 'email', 'first_name',
                  'last_name', 'password']


class GeneralMainUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    rating = serializers.DecimalField(
        read_only=True, max_digits=3, decimal_places=1)
    core_user = GeneralCoreUserSerializer()

    def update(self, instance, validated_data):
        with transaction.atomic():
            instance.bio = validated_data.get('bio', instance.bio)

            if validated_data.get('core_user', None) is not None:
                CoreUser.objects.filter(id=instance.core_user.id).update(
                    first_name=validated_data.get('core_user').get(
                        'first_name', instance.core_user.first_name),
                    last_name=validated_data.get('core_user').get(
                        'last_name', instance.core_user.last_name),
                    password=validated_data.get('core_user').get(
                        'password', instance.core_user.password)
                )

            instance.save()
            return instance

    class Meta:
        model = User
        fields = ['id', 'core_user', 'rating', 'bio']


class CreateCoreUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoreUser
        fields = ['first_name', 'last_name', 'username', 'email', 'password']


class CreateMainUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    core_user = CreateCoreUserSerializer()

    def create(self, validated_data):
        with transaction.atomic():
            core_user_instance = CoreUser.objects.create(
                first_name=validated_data.get('core_user').get('first_name'),
                last_name=validated_data.get('core_user').get('last_name'),
                username=validated_data.get('core_user').get('username'),
                email=validated_data.get('core_user').get('email'),
                password=validated_data.get('core_user').get('password')
            )
            core_user_instance.save()
            instance = User.objects.create(core_user=core_user_instance)
            instance.save()

            cart_instance = Cart.objects.create(student=instance)
            cart_instance.save()

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


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'question_id', 'body']
        read_only_fields = ('id', 'question_id',)


class GeneralQuestionSerializer(serializers.ModelSerializer):
    answer = AnswerSerializer()

    class Meta:
        model = Question
        fields = ['id', 'user_id', 'body', 'answer']
        read_only_fields = ('id', 'user_id', 'answer',)


class AskQuestionSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        instance = Question.objects.create(
            user_id=self.context['user_id'],
            course_id=validated_data['course'].id,
            body=validated_data['body'])

        instance.save()
        return instance

    class Meta:
        model = Question
        fields = ['id', 'body', 'course']
        read_only_fields = ('id',)


class AnswerQuestionSerializer(serializers.ModelSerializer):
    answer = AnswerSerializer()

    def update(self, instance, validated_data):
        body = validated_data['answer']['body']
        question_id = instance.id

        ans_instance = Answer.objects.create(
            question_id=question_id, body=body)

        ans_instance.save()
        return instance

    class Meta:
        model = Question
        fields = ['id', 'user_id', 'body', 'answer']
        read_only_fields = ('id', 'user_id', 'body',)
