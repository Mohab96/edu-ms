# from rest_framework.response import Response
# from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from .serializers import *
from .models import *


class GeneralCourseViewSet(ModelViewSet):
    queryset = Course.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'PUT']:
            return CourseUpdateSerializer
        else:
            return CourseSerializer


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
