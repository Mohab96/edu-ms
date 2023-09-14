# from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from .serializers import *
from .models import *
from django.db import transaction


class GeneralCourseViewSet(ModelViewSet):
    queryset = Course.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'PUT']:
            return CourseUpdateSerializer
        else:
            return CourseSerializer

class CourseItemsViewSet(ModelViewSet):
    serializer_class = CourseContentSerializer

    def get_queryset(self):
        content_id = CourseContent.objects.get(course_id=self.kwargs['course_pk']).id
        return MaterialItem.objects.filter(course_content__id=content_id)

    def get_serializer_context(self):
        return {'content_id': CourseContent.objects.get(course_id=self.kwargs['course_pk']).id}

class GeneralEnrollmentViewSet(ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = GeneralEnrollmentSerializer


class GeneralReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = GeneralReviewSerializer


class CoursesReviewViewSet(ModelViewSet):
    def get_queryset(self):
        return Review.objects.filter(course__id=self.kwargs['course_pk'])

    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'PUT']:
            return ReviewUpdateCoursePrespectiveSerializer
        else:
            return ReviewCoursePrespectiveSerializer

    def get_serializer_context(self):
        return {'course_id': self.kwargs['course_pk']}


class CoursesEnrollmentViewSet(ModelViewSet):
    serializer_class = EnrollmentCoursePrespectiveSerializer

    def get_queryset(self):
        return Enrollment.objects.filter(course__id=self.kwargs['course_pk'])


class GeneralCategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = GeneralCategorySerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateMainUserSerializer
        else:
            return GeneralMainUserSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        with transaction.atomic():
            CoreUser.objects.filter(
                id=instance.core_user.id).delete()
            Cart.objects.filter(
                student__id=instance.id).delete()
            instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk'])

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return UpdateCartItemSerializer
        elif self.request.method == 'POST':
            return CreateCartItemSerializer
        else:
            return CartItemSerializer

    def get_serializer_context(self):
        stud_id = Cart.objects.filter(id=self.kwargs['cart_pk'])[0].student_id
        return {
            'cart_id': self.kwargs['cart_pk'],
            'student_id': stud_id
        }
