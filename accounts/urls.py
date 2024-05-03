from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login, name="login"),
    path('register', views.register, name="register"),
    path('test_token', views.test_token, name="test_token"),
    path('logout', views.logout, name="logout"),
    path('users/<str:user_id>', views.get_user_public_profile, name='get_user_public_profile'),
    path('user-profile/<str:username>', views.get_logged_user_profile, name='get_logged_user_profile'),
    path('home/visible', views.get_visible_users, name='get_visible_users'), 
    path('skills', views.skill_list, name='skill-list'),
    path('skills/<int:pk>', views.skill_detail, name='skill-detail'),
    path('projects', views.project_list, name='project-list'),
    path('projects/<int:pk>', views.project_detail, name='project-detail'),
]
