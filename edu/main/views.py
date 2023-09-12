# from rest_framework.response import Response
# from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from .serializers import *
from .models import *


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'PUT']:
            return CourseUpdateSerializer
        else:
            return CourseSerializer


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'PUT']:
            return ReviewUpdateSerializer
        else:
            return ReviewSerializer

    def get_serializer_context(self):
        return {'course_id': self.kwargs['course_pk']}


class EnrollmentViewSet(ModelViewSet):
    serializer_class = EnrollmentUserPrespectiveSerializer

    def get_queryset(self):
        return Enrollment.objects.filter(course__id=self.kwargs['course_pk'])
