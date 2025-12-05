from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from ..models import Subject, Enrollment, Attendance, Submission, Assignment
from django.contrib import messages  
from ..forms import AssignmentCreateForm

@login_required
def teacher_dashboard(request):
    if request.user.user_type != 'teacher':
        return redirect('student_dashboard')
    subjects = Subject.objects.filter(teacher=request.user)
    return render(request, 'tracker/teacher/dashboard.html', {'subjects': subjects})


@login_required
def mark_attendance(request, subject_id):
    if request.user.user_type != 'teacher':
        return redirect('student_dashboard')

    subject = get_object_or_404(Subject, id=subject_id, teacher=request.user)

    enrollments = Enrollment.objects.filter(subject=subject).select_related('student')

    today = timezone.now().date()

    if request.method == 'POST':
        for enrollment in enrollments:
            student = enrollment.student
            is_present = request.POST.get(f'present_{student.id}') == 'on'

            Attendance.objects.update_or_create(
                student=student,
                subject=subject,
                date=today,
                defaults={'present': is_present}
            )
        return redirect('teacher_dashboard')

    context = {
        'subject': subject,
        'students': enrollments,  
        'today': today,
    }
    return render(request, 'tracker/teacher/attendance.html', context)



@login_required
def grade_submissions(request, assignment_id):
    if request.user.user_type != 'teacher':
        return redirect('student_dashboard')

    assignment = get_object_or_404(Assignment, id=assignment_id, subject__teacher=request.user)
    submissions = Submission.objects.filter(assignment=assignment).select_related('student').order_by('submitted_at')

    if request.method == 'POST':
        submission_id = request.POST.get('submission_id')
        grade = request.POST.get('grade', '').strip()
        feedback = request.POST.get('feedback', '').strip()

        try:
            submission = Submission.objects.get(id=submission_id, assignment=assignment)
            submission.grade = grade or None
            submission.feedback = feedback or None
            submission.graded_at = timezone.now()
            submission.save()

            messages.success(request, f"Grade saved for {submission.student.get_full_name()}!")
        except Submission.DoesNotExist:
            messages.error(request, "Submission not found.")

        return redirect('grade_submissions', assignment_id=assignment.id)

    context = {
        'assignment': assignment,
        'submissions': submissions,
    }
    return render(request, 'tracker/teacher/grade.html', context)


@login_required
def teacher_assignments(request, subject_id):
    if request.user.user_type != 'teacher':
        return redirect('student_dashboard')

    subject = get_object_or_404(Subject, id=subject_id, teacher=request.user)
    assignments = Assignment.objects.filter(subject=subject).order_by('-deadline')

    context = {
        'subject': subject,
        'assignments': assignments,
    }
    return render(request, 'tracker/teacher/assignments_list.html', context)

@login_required
def grade_submissions(request, assignment_id):
    if request.user.user_type != 'teacher':
        return redirect('student_dashboard')

    assignment = get_object_or_404(Assignment, id=assignment_id, subject__teacher=request.user)
    submissions = Submission.objects.filter(assignment=assignment).select_related('student').order_by('student__first_name')

    if request.method == 'POST':
        submission_id = request.POST.get('submission_id')
        if not submission_id:
            messages.error(request, "Invalid submission.")
            return redirect('grade_submissions', assignment_id=assignment.id)

        try:
            sub = Submission.objects.get(id=submission_id, assignment=assignment)
            grade = request.POST.get('grade', '').strip()
            feedback = request.POST.get('feedback', '').strip()

            sub.grade = grade or None
            sub.feedback = feedback or None
            sub.graded_at = timezone.now()
            sub.save()

            messages.success(request, f"Grade saved for {sub.student.get_full_name()}!")
        except Submission.DoesNotExist:
            messages.error(request, "Submission not found.")

        return redirect('grade_submissions', assignment_id=assignment.id)

    context = {
        'assignment': assignment,
        'submissions': submissions,
    }
    return render(request, 'tracker/teacher/grade.html', context)


@login_required
def create_assignment(request, subject_id):
    if request.user.user_type != 'teacher':
        return redirect('student_dashboard')

    subject = get_object_or_404(Subject, id=subject_id, teacher=request.user)

    if request.method == 'POST':
        form = AssignmentCreateForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.subject = subject
            assignment.save()

            messages.success(request, f"Assignment '{assignment.title}' created successfully!")
            return redirect('teacher_assignments', subject_id=subject.id)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = AssignmentCreateForm()

    context = {
        'subject': subject,
        'form': form,
    }
    return render(request, 'tracker/teacher/create_assignment.html', context)