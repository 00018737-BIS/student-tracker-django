from django.urls import path
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login as auth_login
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required

@csrf_protect
def custom_login(request):
    if request.user.is_authenticated:
        user_type = request.user.user_type
        if request.user.is_superuser or user_type == 'admin':
            return redirect('/admin/')
        elif user_type == 'teacher':
            return redirect('teacher_dashboard')
        elif user_type == 'student':
            return redirect('student_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            
            user_type = user.user_type
            if user.is_superuser or user_type == 'admin':
                return redirect('/admin/')
            elif user_type == 'teacher':
                return redirect('teacher_dashboard')
            elif user_type == 'student':
                return redirect('student_dashboard')
            else:
                return redirect('/admin/')
        else:
            return render(request, 'users/login.html', {
                'error': True,
                'form': {'errors': True}
            })
    
    return render(request, 'users/login.html')

@login_required
def home_redirect(request):
    user_type = request.user.user_type
    
    if request.user.is_superuser or user_type == 'admin':
        return redirect('/admin/')
    elif user_type == 'teacher':
        return redirect('teacher_dashboard')
    elif user_type == 'student':
        return redirect('student_dashboard')
    else:
        return redirect('/admin/')

urlpatterns = [
    path('', home_redirect, name='home'),
    path('login/', custom_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]