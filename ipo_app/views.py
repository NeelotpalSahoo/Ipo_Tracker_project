from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
import requests
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework import generics
from .serializers import IPOSerializer
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer
from .models import IPO
from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm  # Import custom form
import requests
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.hashers import make_password

# Home Page
@login_required(login_url='ipo_app:login')  # Redirect to login if not logged in
def home(request):
    ipos = IPO.objects.all()
    serializer = IPOSerializer(ipos, many=True)

    upcoming_ipos = [ipo for ipo in serializer.data if ipo['status'].lower() == 'upcoming']
    ongoing_ipos = [ipo for ipo in serializer.data if ipo['status'].lower() == 'open']
    listed_ipos = [ipo for ipo in serializer.data if ipo['status'].lower() == 'closed']

    return render(request, 'ipo_app/home.html', {
        'upcoming_ipos': upcoming_ipos,
        'ongoing_ipos': ongoing_ipos,
        'listed_ipos': listed_ipos,
    })
    


from django.contrib.auth import login, authenticate

def signup_view(request):
    if request.method == 'POST':
        recaptcha_response = request.POST.get('g-recaptcha-response')
        data = {
            'secret': '6Lfp9nsrAAAAAGOdSVd2HdXYLpJwy07dnfFazmmX',  # Replace with your actual reCAPTCHA secret key
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()
        print("reCAPTCHA result:", result)  # 🔥 Debugging

        form = CustomUserCreationForm(request.POST)
        if form.is_valid() and result.get('success'):
            user = form.save(commit=False)
            user.email = form.cleaned_data.get('email')
            user.save()

            # Authenticate the user before login
            authenticated_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            if authenticated_user is not None:
                login(request, authenticated_user)  # Now Django knows the backend
                messages.success(request, "Signup successful!")
                return redirect('ipo_app:home')
            else:
                messages.error(request, "Authentication failed. Please try logging in.")

        else:
            print("Form errors:", form.errors)  # 🔥 Debugging
            print("reCAPTCHA success:", result.get('success'))  # 🔥 Debugging
            messages.error(request, "Invalid form or reCAPTCHA. Please try again.")
    else:
        form = CustomUserCreationForm()

    return render(request, 'ipo_app/signup.html', {'form': form})

# Login View
def login_view(request):
    if request.user.is_authenticated:
        return redirect('ipo_app:home')  # ✅ Already logged in? Go home.

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('ipo_app:home')  # ✅ Redirect after login
        else:
            messages.error(request, "Invalid credentials. Please try again.")
    else:
        form = AuthenticationForm()

    return render(request, 'ipo_app/login.html', {'form': form})


# Logout View
def logout_view(request):
    logout(request)
    return redirect('ipo_app:login')


# Forgot Password View
def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user_qs = User.objects.filter(email=email)
        if user_qs.exists():
            # Get user
            user = user_qs.first()

            # Generate password reset link
            subject = "Reset Your Bluestock Password"
            email_template_name = "ipo_app/password_reset_email.html"
            context = {
                "email": user.email,
                "domain": request.get_host(),
                "site_name": "Bluestock",
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "user": user,
                "token": default_token_generator.make_token(user),
                "protocol": "https" if request.is_secure() else "http",
            }
            email_body = render_to_string(email_template_name, context)

            # Send Email
            email_msg = EmailMessage(subject, email_body, to=[user.email])
            email_msg.send()

        # Show message whether user exists or not (security best practice)
        messages.success(request, 'If this email is registered, a reset link has been sent.')
        return redirect('ipo_app:forgot_password')

    return render(request, 'ipo_app/forgot_password.html')

def custom_reset_password_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'ipo_app/custom_reset_password.html')

        try:
            user = User.objects.get(username=username)
            user.password = make_password(password1)  # Hash the password
            user.save()
            messages.success(request, "Password successfully reset. You can now log in.")
            return redirect('ipo_app:login')
        except User.DoesNotExist:
            messages.error(request, "User not found.")
            return render(request, 'ipo_app/custom_reset_password.html')

    return render(request, 'ipo_app/custom_reset_password.html')




# Contact Us View
def contact_us_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        # Save to database or send email (optional)
        messages.success(request, 'Your message has been sent. Thank you!')
        return redirect('ipo_app:contact_us')

    return render(request, 'ipo_app/contact_us.html')


# Community View
def community(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.warning(request, "Please login to post.")
            return redirect('ipo_app:login')

        content = request.POST.get('content')
        # Optional: Save post
        messages.success(request, 'Your post has been submitted.')
        return redirect('ipo_app:community')

    return render(request, 'ipo_app/community.html')

class IpoViewSet(viewsets.ModelViewSet):
    queryset = IPO.objects.all()
    serializer_class = IPOSerializer


# API: IPO List
@api_view(['GET'])
@permission_classes([AllowAny])
def ipo_list_api(request):
    ipos = IPO.objects.all()
    serializer = IPOSerializer(ipos, many=True)
    return Response(serializer.data)

def ipo_list_view(request):
    return render(request, 'ipo_app/ipo_list.html')

def user_ipo_list(request):
    return render(request, 'ipo_app/user_ipo_list.html')


def ipo_api_view(request):
    return render(request, 'ipo_app/ipo_api_view.html')


class IPOListAPIView(ListAPIView):
    queryset = IPO.objects.all()
    serializer_class = IPOSerializer

    # API View to get list of IPOs (authenticated)
class IPOListAPIView(generics.ListAPIView):
    queryset = IPO.objects.all()
    serializer_class = IPOSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class IPOCreateView(APIView):
    def post(self, request):
        serializer = IPOSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        serializer = IPOSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)