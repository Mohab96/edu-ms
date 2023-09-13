from django.urls import path
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('courses', views.GeneralCourseViewSet)
router.register('enrollments', views.GeneralEnrollmentViewSet)
router.register('reviews', views.GeneralReviewViewSet)
router.register('categories', views.GeneralCategoryViewSet)
router.register('users', views.UserViewSet)

courses_router = routers.NestedDefaultRouter(
    router, 'courses', lookup='course')

courses_router.register('reviews', views.CoursesReviewViewSet,
                        basename='course-reviews')
courses_router.register('enrollments', views.CoursesEnrollmentViewSet,
                        basename='course-enrollments')

# URLConf
urlpatterns = router.urls + courses_router.urls
