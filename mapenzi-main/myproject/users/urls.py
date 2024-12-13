from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from django.contrib.auth import logout

from .views import custom_logout

app_name = 'users'

urlpatterns = [
    # General paths
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', custom_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('enrollment/', views.enrollment, name='enrollment'),

    # Course-related paths
    path('courses/', views.course, name='course'),  # List all courses
     path('create-announcement/', views.create_announcement, name='create_announcement'),
    path('announcement/edit/<int:id>/', views.edit_announcement, name='edit_announcement'),
    path('announcement/delete/<int:id>/', views.delete_announcement, name='delete_announcement'),
]

# The second block is redundant and can be removed.
