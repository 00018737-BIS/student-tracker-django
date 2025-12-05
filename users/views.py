from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

@login_required
def home_redirect(request):
    """
    Smart redirect after login based on user_type
    """
    if request.user.user_type == 'student':
        return redirect('student_dashboard')
    elif request.user.user_type == 'teacher':
        return redirect('teacher_dashboard')
    else:
        return redirect('admin:index')