from django.urls import path
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('courses', views.CourseViewSet)

courses_router = routers.NestedDefaultRouter(
    router, 'courses', lookup='course')

courses_router.register('reviews', views.ReviewViewSet,
                        basename='course-reviews')
courses_router.register('enrollments', views.EnrollmentViewSet,
                        basename='course-enrollments')

# URLConf
urlpatterns = router.urls + courses_router.urls
