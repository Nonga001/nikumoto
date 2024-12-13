from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import Group
from .models import Course, Announcement
from .forms import CourseForm, UserRegistrationForm, AnnouncementForm

# User Authentication and Registration Views
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = None  # Set role to None explicitly
            user.save()
            return redirect('login')  # Redirect to login after registration
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')  # Redirect to dashboard
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

# Home and Profile Views
@login_required
def home(request):
    user = request.user
    role = None
    functions = []

    if user.groups.filter(name='lecturers').exists():
        role = "lecturers"
        functions = [
            "View Announcements",
            "Create Announcement",
            "Edit Announcement",
            "Delete Your Announcement",
        ]
    elif user.groups.filter(name='students').exists():
        role = "students"
        functions = ["View Announcements"]

    announcements = Announcement.objects.all().order_by('-created_at')

    context = {
        'role': role,
        'functions': functions,
        'announcements': announcements,
    }
    return render(request, 'home.html', context)


@login_required
def profile(request):
    user = request.user
    groups = user.groups.values_list('name', flat=True)

    # Debugging output to ensure groups are correct
    print(f"User Groups: {groups}")

    # Assign role based on the user's group, only 'lecturers' or 'students'
    if 'lecturers' in groups:
        role = 'lecturers'
    elif 'students' in groups:
        role = 'students'
    else:
        role = None  # No role will be assigned if neither group is found

    # More debugging to ensure role is correctly set
    print(f"Assigned Role: {role}")

    context = {
        'role': role,
        'date_joined': user.date_joined,
        'last_login': user.last_login,
    }
    return render(request, 'profile.html', context)
# Announcement Views
@login_required
def create_announcement(request):
    if request.user.groups.filter(name='lecturers').exists():
        if request.method == 'POST':
            form = AnnouncementForm(request.POST)
            if form.is_valid():
                announcement = form.save(commit=False)
                announcement.creator = request.user
                announcement.save()
                return redirect('home')
        else:
            form = AnnouncementForm()
        return render(request, 'create_announcement.html', {'form': form})
    return redirect('home')

@login_required
def edit_announcement(request, id):
    announcement = get_object_or_404(Announcement, id=id)
    if announcement.creator != request.user:
        return redirect('home')
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AnnouncementForm(instance=announcement)
    return render(request, 'edit_announcement.html', {'form': form, 'announcement': announcement})

@login_required
def delete_announcement(request, id):
    announcement = get_object_or_404(Announcement, id=id)
    if announcement.creator != request.user:
        return redirect('home')
    if request.method == 'POST':
        announcement.delete()
        return redirect('home')
    return render(request, 'confirm_delete.html', {'announcement': announcement})

def course(request):
    courses = Course.objects.all()  # Fetch all courses
    return render(request, 'course.html', {'courses': courses})

def enrollment(request):
    # Logic for the enrollment page
    return render(request, 'enrollment.html')

def custom_logout(request):
    logout(request)
    return redirect('users:login')  # Redirect to the homepage or wherever you want
