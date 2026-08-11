from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    StudentViewSet, CourseViewSet, EnrollmentViewSet,
    AssignmentViewSet, SubmissionViewSet
)

router = DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'enrollments', EnrollmentViewSet)
router.register(r'assignments', AssignmentViewSet)
router.register(r'submissions', SubmissionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
