from django.urls import path
from tracker.views.teacher_views import (
    teacher_dashboard,
    mark_attendance,
    teacher_assignments,      
    grade_submissions,
    create_assignment,
)

urlpatterns = [
    path('', teacher_dashboard, name='teacher_dashboard'),
    path('assignments/<int:subject_id>/', teacher_assignments, name='teacher_assignments'),
    path('grade-submissions/<int:assignment_id>/', grade_submissions, name='grade_submissions'),
    path('mark-attendance/<int:subject_id>/', mark_attendance, name='mark_attendance'),
    path('teacher/subject/<int:subject_id>/assignments/create/', create_assignment, name='create_assignment'),
]
