# ipo_app/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IpoViewSet
from rest_framework.authtoken.views import obtain_auth_token
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

app_name = 'ipo_app'

# Register the API ViewSet
router = DefaultRouter()
router.register(r'ipos', IpoViewSet, basename='ipo')

urlpatterns = [
    # Website routes
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('contact-us/', views.contact_us_view, name='contact_us'),
    path('community/', views.community, name='community'),
    path('ipos/', views.ipo_list_view, name='ipo_list'),


    # API endpoints
    path('api/', include(router.urls)),  # This handles /api/ipos/
    path('api/token-auth/', obtain_auth_token),
    path('auth/', include('social_django.urls', namespace='social')), 
    # Forgot password flow
    path('reset-password/', views.custom_reset_password_view, name='reset_password'),
    path('forgot-password/', views.custom_reset_password_view, name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
    template_name='ipo_app/password_reset_confirm.html',
    success_url='/login/'
    ), name='password_reset_confirm'),
]