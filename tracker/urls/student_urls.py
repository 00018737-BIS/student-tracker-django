from django.urls import path
from tracker.views.student_views import (
    student_dashboard,
    subject_list,
    attendance_view,
    grades_view,
    assignment_list,
    submit_assignment,
)

urlpatterns = [
    path('', student_dashboard, name='student_dashboard'),           # Main landing page
    path('subjects/', subject_list, name='subject_list'),           # Optional: list view
    path('attendance/<int:subject_id>/', attendance_view, name='attendance'),
    path('grades/', grades_view, name='grades'),
    path('assignments/<int:subject_id>/', assignment_list, name='assignments_by_subject'),
    path('assignment/submit/<int:assignment_id>/', submit_assignment, name='submit_assignment'),
]