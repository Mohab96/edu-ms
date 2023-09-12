# from rest_framework.response import Response
# from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
# from .permissions import IsAdminOrOwner
from .serializers import *
from .models import *


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()

    # def get_permissions(self):
    #     if self.request.method in ['PUT', 'PATCH', 'DELETE']:
    #         # must be an admin or created this course
    #         return [IsAdminOrOwner()]
    #     else:
    #         return [AllowAny()]

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
