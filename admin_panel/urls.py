from django.urls import path
from . import views
from django.urls import path, include
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from .api_views import IPOListAPIView
from .views import admin_register_ipo

app_name = 'admin_panel'

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.admin_signup_view, name='signup'),
    path('login/', views.admin_login_view, name='login'),
    path('forgot-password/', views.admin_forgot_password_view, name='forgot_password'),
    path('dashboard/', views.admin_dashboard, name='dashboard'),
    path('logout/',  views.logout_view,         name='admin_logout'),

    path('api/ipo/', views.ipo_list_api, name='ipo_list_api'),
    
    # path('upcoming-ipos/', views.admin_upcoming_ipos, name='admin_upcoming_ipos'),
    path('upcoming-ipos/', views.admin_upcoming_ipos, name='admin_upcoming_ipos'),
    path('upcoming-ipos/edit/<int:ipo_id>/', views.edit_ipo, name='edit_ipo'),
    path('upcoming-ipos/delete/<int:ipo_id>/', views.delete_ipo, name='delete_ipo'),
    path('register-ipo/', views.admin_register_ipo, name='admin_register_ipo'),
    path('users/', views.admin_users, name='admin_users'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('manage-ipo/', views.admin_manage_ipo, name='admin_manage_ipo'),
    path('manage-ipo/ipo-information/', views.register_ipo, name='register_ipo'),
    path('register-ipo/', views.register_ipo, name='admin_register_ipo'),
    path('manage-ipo/', views.manage_ipo, name='manage_ipo'),
    path('edit-ipo/<int:ipo_id>/', views.edit_ipo, name='edit_ipo'),
    path('delete-ipo/<int:ipo_id>/', views.delete_ipo, name='delete_ipo'),
    path('manage-ipo/', views.manage_ipo_view, name='admin_manage_ipo'),
    path('view-ipo/<int:ipo_id>/', views.view_ipo, name='view_ipo'),
    path('admin/manage-ipos/', views.admin_manage_ipo, name='admin_manage_ipo'),
    path('api/ipos/', IPOListAPIView.as_view(), name='ipo_list_api'),  # <-- Your API endpoint
    path('admin-panel/register-ipo/', admin_register_ipo, name='register_ipo'),
]