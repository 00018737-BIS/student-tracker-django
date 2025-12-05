from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tracker.views.api_views import SubjectViewSet, AssignmentViewSet, SubmissionViewSet

router = DefaultRouter()
router.register(r'subjects', SubjectViewSet)
router.register(r'assignments', AssignmentViewSet)
router.register(r'submissions', SubmissionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]