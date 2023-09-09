# from rest_framework.response import Response
# from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from .serializers import *
from .models import *


class CourseViewSet(ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
