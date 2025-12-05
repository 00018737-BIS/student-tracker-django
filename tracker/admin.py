from django.contrib import admin
from .models import Subject, Enrollment, Assignment, Submission, Attendance

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'teacher')

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject')

admin.site.register(Assignment)
admin.site.register(Submission)
admin.site.register(Attendance)