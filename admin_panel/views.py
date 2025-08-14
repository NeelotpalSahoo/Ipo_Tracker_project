from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .models import IPO
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .forms import IPOForm
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
import logging
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework import generics
from .models import IPO
from .serializers import IPOSerializer
from django.http import HttpResponse
from datetime import datetime
from decimal import Decimal, InvalidOperation
from .form import CustomUserCreationForm  # Import custom form
import requests

# Home page
def home(request):
    ipos = IPO.objects.all()
    return render(request, 'ipo_app/home.html', {'ipos': ipos})

# Signup
def admin_signup_view(request):
    if request.method == 'POST':
        recaptcha_response = request.POST.get('g-recaptcha-response')
        data = {
            'secret': '6Lfp9nsrAAAAAGOdSVd2HdXYLpJwy07dnfFazmmX',  # Replace with your reCAPTCHA secret key
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()
        print("🔒 reCAPTCHA result:", result)  # Debugging

        form = CustomUserCreationForm(request.POST)
        if form.is_valid() and result.get('success'):
            user = form.save(commit=False)
            user.is_staff = True  # ✅ Make user an admin
            user.email = form.cleaned_data.get('email')
            user.save()

            # Authenticate and login
            authenticated_user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            if authenticated_user is not None:
                login(request, authenticated_user)
                messages.success(request, "Signup successful! Welcome to Bluestock Admin Panel.")
                return redirect('admin_panel:dashboard')
            else:
                messages.error(request, "✅ Signup worked but authentication failed. Try logging in manually.")
        else:
            print("⚠️ Form errors:", form.errors)  # Debugging
            print("⚠️ reCAPTCHA success:", result.get('success'))  # Debugging
            messages.error(request, "Invalid form data or reCAPTCHA failed. Please try again.")
    else:
        form = CustomUserCreationForm()

    return render(request, 'admin_panel/signup.html', {'form': form})
# Login
def admin_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('admin_panel:dashboard')
        else:
            messages.error(request, "Invalid credentials")
    else:
        form = AuthenticationForm()

    return render(request, 'admin_panel/login.html', {'form': form})
# Logout
def logout_view(request):
    logout(request)
    return redirect('admin_panel:login')

# Forgot password
def admin_forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        messages.success(request, 'If this email is registered, a reset link has been sent.')
        return redirect('admin_panel:forgot_password')
    return render(request, 'admin_panel/forgot_password.html')

logger = logging.getLogger(__name__)

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    logger.info(f"User {user.username} logged in at {user.last_login}")

# IPO List API
def ipo_list_api(request):
    ipos = IPO.objects.all().values('id', 'company_name', 'status', 'open_date', 'close_date', 'logo')
    return JsonResponse(list(ipos), safe=False)

# Admin Dashboard
def admin_dashboard(request):
    ipos = IPO.objects.all()
    
    return render(request, 'admin_panel/dashboard.html')

# Upcoming IPOs
def admin_upcoming_ipos(request):
    ipos = IPO.objects.filter(status='Upcoming')
    return render(request, 'admin_panel/upcoming_ipos.html')

# Register IPO
def admin_register_ipo(request):
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        price_band = request.POST.get('price_band')
        issue_size = request.POST.get('issue_size')
        open_date = request.POST.get('open_date')
        close_date = request.POST.get('close_date')
        status = request.POST.get('status')

        IPO.objects.create(
            company_name=company_name,
            price_band=price_band,
            issue_size=issue_size,
            open_date=open_date,
            close_date=close_date,
            status=status
        )
        return redirect('admin_panel:admin_upcoming_ipos')
    return render(request, 'admin_panel/register_ipo.html')

# Users page in admin
def admin_users(request):
    return render(request, 'admin_panel/users.html')

# List IPOs
def admin_ipos_list(request):
    ipos = IPO.objects.all()
    return render(request, 'admin_panel/admin_ipos_list.html', {'ipos': ipos})

def get_decimal_or_none(value):
    try:
        return Decimal(value.strip()) if value and value.strip() else None
    except (InvalidOperation, AttributeError):
        return None


def admin_register_ipo(request):
    if request.method == 'POST':
        try:
            company_name = request.POST.get('company_name')
            price_band = request.POST.get('price_band')
            open_date = datetime.strptime(request.POST.get('open_date').strip(), "%Y-%m-%d").date()
            close_date = datetime.strptime(request.POST.get('close_date').strip(), "%Y-%m-%d").date()
            listing_date = datetime.strptime(request.POST.get('listing_date').strip(), "%Y-%m-%d").date()

            issue_size = request.POST.get('issue_size')
            issue_type = request.POST.get('issue_type')
            status = request.POST.get('status')

            ipo_price = get_decimal_or_none(request.POST.get('ipo_price'))
            listing_price = get_decimal_or_none(request.POST.get('listing_price'))
            listing_gain = get_decimal_or_none(request.POST.get('listing_gain'))
            current_return = get_decimal_or_none(request.POST.get('current_return'))
            cmp = get_decimal_or_none(request.POST.get('cmp'))

            final_listing_date_str = request.POST.get('final_listing_date')
            final_listing_date = (
                datetime.strptime(final_listing_date_str.strip(), "%Y-%m-%d").date()
                if final_listing_date_str and final_listing_date_str.strip() else None
            )

            rhp_link = request.POST.get('rhp_link')
            drhp_link = request.POST.get('drhp_link')
            logo = request.FILES.get('logo')

            ipo = IPO(
                company_name=company_name,
                price_band=price_band,
                open_date=open_date,
                close_date=close_date,
                listing_date=listing_date,
                issue_size=issue_size,
                issue_type=issue_type,
                status=status,
                ipo_price=ipo_price,
                listing_price=listing_price,
                listing_gain=listing_gain,
                current_return=current_return,
                cmp=cmp,
                final_listing_date=final_listing_date,
                rhp_link=rhp_link,
                drhp_link=drhp_link,
                logo=logo
            )
            ipo.save()
            return HttpResponse("IPO registered successfully!")

        except Exception as e:
            return HttpResponse(f"Error: {str(e)}")

    # GET request — render the form template
    return render(request, 'admin_panel/register_ipo.html')

# View: Upcoming IPOs
def admin_upcoming_ipos(request):
    ipos = IPO.objects.filter(status='Upcoming')
    return render(request, 'admin_panel/upcoming_ipos.html', {
        'ipos': ipos
    })

def admin_manage_ipo(request):
    query = request.GET.get('q', '').strip()
    
    if query:
        ipos = IPO.objects.filter(company_name__icontains=query)
    else:
        ipos = IPO.objects.all()

    return render(request, 'admin_panel/manage_ipos.html', {'ipos': ipos})

def register_ipo(request):
    if request.method == 'POST':
        form = IPOForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:admin_manage_ipo')  # Redirect to IPO list
    else:
        form = IPOForm()
    
    return render(request, 'admin_panel/register_ipo.html', {'form': form})

def manage_ipo(request):
    # your logic here
    return render(request, 'admin_panel/manage_ipo.html')

def manage_ipo_view(request):
    ipos = IPO.objects.all()
    return render(request, 'admin_panel/manage_ipo.html', {'ipos': ipos})

def manage_ipo_dashboard(request):
    ipos = IPO.objects.all().order_by('-id')  # Fetch all IPOs
    return render(request, 'admin_panel/manage_ipo.html', {'ipos': ipos})


# Edit IPO View
def edit_ipo(request, ipo_id):
    ipo = IPO.objects.get(id=ipo_id)
    if request.method == 'POST':
        ipo.company_name = request.POST.get('company_name')
        ipo.price_band = request.POST.get('price_band')
        ipo.open_date = request.POST.get('open_date')
        ipo.close_date = request.POST.get('close_date')
        ipo.issue_size = request.POST.get('issue_size')
        ipo.issue_type = request.POST.get('issue_type')
        ipo.listing_date = request.POST.get('listing_date')
        ipo.status = request.POST.get('status')
        ipo.ipo_price = request.POST.get('ipo_price')
        ipo.listing_price = request.POST.get('listing_price')
        ipo.listing_gain = request.POST.get('listing_gain')
        ipo.current_return = request.POST.get('current_return')
        ipo.cmp = request.POST.get('cmp')
        ipo.final_listing_date = request.POST.get('final_listing_date')
        ipo.rhp_link = request.POST.get('rhp_link')
        ipo.drhp_link = request.POST.get('drhp_link')
        ipo.save()
        return redirect('admin_panel:manage_ipo')

    return render(request, 'admin_panel/edit_ipo.html', {'ipo': ipo})

# Delete IPO View
def delete_ipo(request, ipo_id):
    ipo = IPO.objects.get(id=ipo_id)
    ipo.delete()
    return redirect('admin_panel:manage_ipo')

    
def view_ipo(request, ipo_id):
    ipo = get_object_or_404(IPO, id=ipo_id)
    return render(request, 'admin_panel/view_ipo.html', {'ipo': ipo})

def admin_upcoming_ipos(request):
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        price_band = request.POST.get('price_band')
        open_date = request.POST.get('open_date') or None
        close_date = request.POST.get('close_date') or None
        issue_size = request.POST.get('issue_size')
        issue_type = request.POST.get('issue_type')
        listing_date = request.POST.get('listing_date') or None
        status = request.POST.get('status')
        ipo_price = request.POST.get('ipo_price') or None
        listing_price = request.POST.get('listing_price') or None
        listing_gain = request.POST.get('listing_gain')
        current_return = request.POST.get('current_return')
        cmp = request.POST.get('cmp')
        rhp_pdf_link = request.POST.get('rhp_pdf_link')
        drhp_pdf_link = request.POST.get('drhp_pdf_link')
        logo = request.FILES.get('logo')

        ipo = IPO(
            company_name=company_name,
            price_band=price_band,
            open_date=open_date,
            close_date=close_date,
            issue_size=issue_size,
            issue_type=issue_type,
            listing_date=listing_date,
            status=status,
            ipo_price=ipo_price,
            listing_price=listing_price,
            listing_gain=listing_gain,
            current_return=current_return,
            cmp=cmp,
            rhp_pdf_link=rhp_pdf_link,
            drhp_pdf_link=drhp_pdf_link,
            logo=logo
        )
        ipo.save()
        messages.success(request, "IPO Registered Successfully!")
        return redirect('admin_upcoming_ipos')

    return render(request, 'admin_panel/upcoming_ipos.html')