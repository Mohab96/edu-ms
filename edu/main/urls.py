from django.urls import path
from rest_framework_nested import routers
from . import views


router = routers.DefaultRouter()
router.register('courses', views.CourseViewSet)

# URLConf
urlpatterns = router.urls
