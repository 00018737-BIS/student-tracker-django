from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from ..models import Subject, Enrollment, Attendance, Submission, Assignment

@login_required
def student_dashboard(request):
    """Modern Card-based Student Dashboard - Main Landing Page"""
    if request.user.user_type != 'student':
        return redirect('teacher_dashboard')

    enrollments = Enrollment.objects.filter(
        student=request.user
    ).select_related('subject', 'subject__teacher')

    enhanced_enrollments = []
    now = timezone.now()

    for enrollment in enrollments:
        subject = enrollment.subject

        attendance_records = Attendance.objects.filter(
            student=request.user,
            subject=subject
        )
        total = attendance_records.count()
        present = attendance_records.filter(present=True).count()
        attendance_pct = (present / total * 100) if total > 0 else 0

        pending_assignments = Assignment.objects.filter(
            subject=subject,
            deadline__gte=now
        ).exclude(
            submission__student=request.user
        ).count()

        overdue_assignments = Assignment.objects.filter(
            subject=subject,
            deadline__lt=now
        ).exclude(
            submission__student=request.user
        ).count()

        enhanced_enrollments.append({
            'subject': subject,
            'teacher_name': subject.teacher.get_full_name() or subject.teacher.username,
            'attendance_percentage': round(attendance_pct, 1),
            'pending_assignments': pending_assignments,
            'overdue_assignments': overdue_assignments,
            'total_assignments': Assignment.objects.filter(subject=subject).count(),
        })

    context = {
        'enrolled_subjects': enhanced_enrollments,
        'total_subjects': len(enhanced_enrollments),
    }
    return render(request, 'tracker/student/dashboard.html', context)

@login_required
def subject_list(request):
    """List all enrolled subjects"""
    if request.user.user_type != 'student':
        return redirect('teacher_dashboard')
    
    subjects = Subject.objects.filter(
        enrollment__student=request.user
    ).select_related('teacher')
    
    return render(request, 'tracker/student/subjects.html', {'subjects': subjects})


@login_required
def attendance_view(request, subject_id):
    """View attendance records for a specific subject"""
    if request.user.user_type != 'student':
        return redirect('teacher_dashboard')
    
    subject = get_object_or_404(Subject, id=subject_id)
    
    if not Enrollment.objects.filter(student=request.user, subject=subject).exists():
        messages.error(request, "You are not enrolled in this subject.")
        return redirect('subject_list')
    
    records = Attendance.objects.filter(
        student=request.user,
        subject=subject
    ).order_by('-date')
    
    total_count = records.count()
    present_count = records.filter(present=True).count()
    absent_count = records.filter(present=False).count()
    attendance_percentage = (present_count / total_count * 100) if total_count > 0 else 0
    
    context = {
        'records': records,
        'subject': subject,
        'present_count': present_count,
        'absent_count': absent_count,
        'attendance_percentage': attendance_percentage,
    }
    return render(request, 'tracker/student/attendance.html', context)


@login_required
def grades_view(request):
    """View all graded submissions"""
    if request.user.user_type != 'student':
        return redirect('teacher_dashboard')
    
    submissions = Submission.objects.filter(
        student=request.user
    ).select_related('assignment', 'assignment__subject').order_by('-submitted_at')
    
    return render(request, 'tracker/student/grades.html', {'submissions': submissions})


@login_required
def assignment_list(request, subject_id=None):
    """List all assignments for a specific subject"""
    if request.user.user_type != 'student':
        return redirect('teacher_dashboard')

    now = timezone.now()

    if subject_id:
        subject = get_object_or_404(Subject, id=subject_id)
        if not Enrollment.objects.filter(student=request.user, subject=subject).exists():
            messages.error(request, "You are not enrolled in this subject.")
            return redirect('student_dashboard')
        
        assignments = Assignment.objects.filter(subject=subject).select_related('subject').order_by('deadline')
    else:
        assignments = Assignment.objects.filter(subject__enrollment__student=request.user).select_related('subject').order_by('deadline')
        subject = None

    submitted_ids = Submission.objects.filter(student=request.user).values_list('assignment_id', flat=True)
    for assignment in assignments:
        assignment.is_submitted = assignment.id in submitted_ids
        assignment.is_overdue = assignment.deadline < now and not assignment.is_submitted

    return render(request, 'tracker/student/assignments.html', {
        'assignments': assignments,
        'subject': subject
    })


@login_required
def submit_assignment(request, assignment_id):
    """Submit an assignment"""
    if request.user.user_type != 'student':
        return redirect('teacher_dashboard')
    
    assignment = get_object_or_404(Assignment, id=assignment_id)
    
    if not Enrollment.objects.filter(student=request.user, subject=assignment.subject).exists():
        messages.error(request, "You are not enrolled in this subject.")
        return redirect('assignments_by_subject', subject_id=assignment.subject.id)
    
    if Submission.objects.filter(student=request.user, assignment=assignment).exists():
        messages.warning(request, "You have already submitted this assignment.")
        return redirect('assignments_by_subject', subject_id=assignment.subject.id)
    
    if request.method == 'POST':
        if 'file' not in request.FILES:
            messages.error(request, "Please select a file to upload.")
            return render(request, 'tracker/student/submit.html', {'assignment': assignment})
        
        file = request.FILES['file']
        
        Submission.objects.create(
            assignment=assignment,
            student=request.user,
            file=file
        )
        
        messages.success(request, f"Assignment '{assignment.title}' submitted successfully!")
        return redirect('assignments_by_subject', subject_id=assignment.subject.id)
    
    assignment.is_overdue = assignment.deadline < timezone.now()
    
    return render(request, 'tracker/student/submit.html', {'assignment': assignment})

