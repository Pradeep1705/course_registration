from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from core.models import Course,Registration, User
from django.contrib.auth.hashers import make_password

def landing_page(request):
    return render(request, 'landing.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            if user.role == 'student':
                return redirect('student_dashboard')
            else:
                return redirect('faculty_dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username already exists'})
        if User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': 'Email already registered'})
        
        if email.endswith('@ds.study.iitm.ac.in'):
            role = 'student'
        elif email.endswith('@pod.iitm.ac.in'):
            role = 'faculty'
        else:
            return render(request, 'signup.html', {'error': 'Enter a valid email address'})

        user = User.objects.create(
            username=username,
            password=make_password(password),
            email=email,
            role=role
        )
        login(request, user)
        if role == 'student':
            return redirect('student_dashboard')
        else:
            return redirect('faculty_dashboard')

    return render(request, 'signup.html')

@login_required
def offer_course(request):
    if request.user.role != 'faculty':
        return redirect('login')
    
    if request.method == "POST":
        name = request.POST['name']
        code = request.POST['code']

        if Course.objects.filter(name=name).exists():
            return render(request, 'faculty_course_offer.html', {
                'error': 'Course name already exists.'
            })

        if Course.objects.filter(code=code).exists():
            return render(request, 'faculty_course_offer.html', {
                'error': 'Course code already exists.'
            })

        Course.objects.create(name=name, code=code, faculty=request.user)
        return redirect('faculty_dashboard')
    return render(request, 'faculty_course_offer.html')

@login_required
def register_course(request):
    if request.user.role != 'student':
        return redirect('login')

    registered_courses = Registration.objects.filter(student=request.user).count()
    courses = Course.objects.exclude(registration__student=request.user)

    if request.method == "POST":
        if registered_courses == 2:
            return render(request, 'student_register.html', {
                'courses': courses,
                'error': 'You can only register for 2 courses.'
            })
        
        course_id = request.POST['course_id']
        course = Course.objects.get(id=course_id)
        Registration.objects.create(student=request.user, course=course)
        return redirect('student_dashboard')

    return render(request, 'student_register.html', {'courses': courses})


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def student_dashboard(request):
    if request.user.role != 'student':
        return redirect('login')
    registrations = Registration.objects.filter(student=request.user).select_related('course__faculty')
    return render(request, 'dashboard.html', {'registrations': registrations})

@login_required
def faculty_dashboard(request):
    if request.user.role != 'faculty':
        return redirect('login') 
    courses = Course.objects.filter(faculty=request.user)

    # Manually count registered students for each course
    course_data = []
    for course in courses:
        count = Registration.objects.filter(course=course).count()
        course_data.append({
            'code': course.code,
            'name': course.name,
            'count': count
        })

    return render(request, 'dashboard.html', {'courses': course_data})

