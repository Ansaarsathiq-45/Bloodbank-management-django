from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from datetime import date, timedelta

from .models import Donor, Patient, BloodStock, BloodDonation, BloodRequest
from .forms import DonorSignupForm, PatientSignupForm, BloodStockForm, BloodRequestForm, BloodDonationForm


# Home Page
def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'home.html')


# Donor Signup
def donor_signup(request):
    if request.method == "POST":
        form = DonorSignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Donor registered successfully. Wait for admin approval.")
            return redirect('donor_login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = DonorSignupForm()
    return render(request, 'donor_signup.html', {'form': form})


# Donor Login
def donor_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user and hasattr(user, 'donor'):
            if user.donor.is_approved:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "Your account is not approved by admin yet.")
        else:
            messages.error(request, "Invalid credentials or not a donor.")
    return render(request, 'donor_login.html')


# Patient Signup
def patient_signup(request):
    if request.method == "POST":
        form = PatientSignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Patient registered successfully. Wait for admin approval.")
            return redirect('patient_login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PatientSignupForm()
    return render(request, 'patient_signup.html', {'form': form})


# Patient Login
def patient_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user and hasattr(user, 'patient'):
            if user.patient.is_approved:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "Your account is not approved by admin yet.")
        else:
            messages.error(request, "Invalid credentials or not a patient.")
    return render(request, 'patient_login.html')


# Logout
def user_logout(request):
    logout(request)
    return redirect('home')


# Dashboard
@login_required
def dashboard(request):
    donors = Donor.objects.all()
    patients = Patient.objects.all()
    stocks = BloodStock.objects.all()

    if hasattr(request.user, 'donor'):
        user_name = request.user.donor.name
    elif hasattr(request.user, 'patient'):
        user_name = request.user.patient.name
    else:
        user_name = request.user.first_name or request.user.username

    context = {
        'donors': donors,
        'patients': patients,
        'stocks': stocks,
        'user_name': user_name,
    }
    return render(request, 'dashboard.html', context)


# Manage Blood Stock
@login_required
def manage_blood_stock(request):
    if request.method == "POST":
        form = BloodStockForm(request.POST)
        if form.is_valid():
            blood_group = form.cleaned_data['blood_group']
            units = form.cleaned_data['units']
            stock, _ = BloodStock.objects.get_or_create(blood_group=blood_group)
            stock.units = units
            stock.save()
            messages.success(request, "Blood stock updated successfully.")
            return redirect('manage_blood_stock')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = BloodStockForm()
    stocks = BloodStock.objects.all()
    return render(request, 'manage_blood_stock.html', {'form': form, 'stocks': stocks})


# Donate Blood (Donor)
@login_required
def donate_blood(request):
    try:
        donor = request.user.donor
    except Donor.DoesNotExist:
        messages.error(request, "Only registered donors can donate blood.")
        return redirect('dashboard')

    if not donor.is_approved:
        messages.warning(request, "Your account is not approved by admin yet.")
        return redirect('dashboard')

    last_donation = BloodDonation.objects.filter(donor=donor).order_by('-date_donated').first()
    if last_donation and (date.today() - last_donation.date_donated) < timedelta(days=90):
        messages.warning(request, "You can donate again after 3 months from your last donation.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = BloodDonationForm(request.POST)
        if form.is_valid():
            units = form.cleaned_data['units_donated']

            with transaction.atomic():
                # Save donation
                BloodDonation.objects.create(donor=donor, blood_group=donor.blood_group, units_donated=units)

                # Update stock
                stock, _ = BloodStock.objects.get_or_create(blood_group=donor.blood_group)
                stock.units += units
                stock.save()

            messages.success(request, "Thank you for donating blood!")
            return redirect('dashboard')
        else:
            messages.error(request, "Please enter a valid number of units.")
    else:
        form = BloodDonationForm()

    return render(request, 'donate_blood.html', {'donor': donor, 'form': form})


# Blood Request (Patient)
@login_required
def blood_request_view(request):
    try:
        patient = request.user.patient
    except Patient.DoesNotExist:
        messages.error(request, "Only registered patients can request blood.")
        return redirect('home')

    if not patient.is_approved:
        messages.warning(request, "Your account is not approved by admin yet.")
        return redirect('home')

    if request.method == 'POST':
        form = BloodRequestForm(request.POST)
        if form.is_valid():
            blood_group = form.cleaned_data['blood_group']
            units_requested = form.cleaned_data['units_requested']

            stock = BloodStock.objects.filter(blood_group=blood_group).first()
            available_units = stock.units if stock else 0

            if available_units < units_requested:
                messages.error(request, f"Not enough {blood_group} blood available. Only {available_units} units left.")
                return redirect('blood_request')

            with transaction.atomic():
                # Reduce stock
                stock.units -= units_requested
                stock.save()

                # Save request as Approved
                BloodRequest.objects.create(
                    patient=patient,
                    blood_group=blood_group,
                    units_requested=units_requested,
                    status='Approved'
                )

            messages.success(request, f"{units_requested} units of {blood_group} blood issued successfully.")
            return redirect('dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = BloodRequestForm()

    return render(request, 'blood_request.html', {'form': form, 'patient': patient})
