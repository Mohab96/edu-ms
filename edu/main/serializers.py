from rest_framework import serializers
from .models import *
from core.models import CoreUser
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status


class MaterialItemSerializer(serializers.ModelSerializer):
    file = serializers.FileField()

    def create(self, validated_data):
        content_id = self.context['content_id']
        return MaterialItem.objects.create(course_content_id=content_id, **validated_data)

    class Meta:
        model = MaterialItem
        fields = ['file']


class CourseContentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    course_id = serializers.IntegerField(read_only=True)
    items = MaterialItemSerializer(many=True, read_only=True)

    class Meta:
        model = CourseContent
        fields = ['id', 'course_id', 'items']


class CourseSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    content = CourseContentSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'created_by', 'last_update',
                  'requirements', 'objectives', 'price', 'category',
                  'welcome_message', 'content']


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
        return self.context['student_id']

    class Meta:
        model = CartItem
        fields = ['id', 'student_id', 'course_id']


class CreateCartItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    cart_id = serializers.SerializerMethodField(read_only=True)

    def get_cart_id(self, cart):
        return self.context['cart_id']

    def create(self, validated_data):
        condition = CartItem.objects \
            .filter(cart_id=validated_data['cart_id']) \
            .filter(course_id=validated_data['course_id']) \
            .exists()

        if condition:
            return Response(status=status.HTTP_204_NO_CONTENT)

        with transaction.atomic():
            instance = CartItem.objects.create(**validated_data)
            instance.save()

        return instance

    class Meta:
        model = CartItem
        fields = ['id', 'cart_id', 'course_id']


class UpdateCartItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    cart_id = serializers.SerializerMethodField(read_only=True)

    def get_cart_id(self, cart):
        return self.context['cart_id']

    def update(self, instance, validated_data):
        print(instance.__dict__, dict(validated_data))

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

                    old_price = Course.objects \
                        .filter(id=current_course_id)[0].price

                    new_price = Course.objects \
                        .filter(id=new_course_id)[0].price

                    current_cart_price = Cart.objects \
                        .filter(id=instance.cart_id)[0].total_price

                    current_cart_price -= old_price
                    current_cart_price += new_price

                    Course.objects \
                        .filter() \
                        .update(total_price=current_cart_price)

                    instance.save()
            else:
                CartItem.objects.filter(id=instance.id).delete()
                return Response(status=status.HTTP_204_NO_CONTENT)

        return instance

    class Meta:
        model = CartItem
        fields = ['id', 'cart_id', 'course_id']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'student_id', 'items']


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

    # created_by = CourseSerializer(many=True, read_only=True)
    # enrolled_in = CourseSerializer(many=True, read_only=True)

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
        # 'created_by' , 'enrolled_in'


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
