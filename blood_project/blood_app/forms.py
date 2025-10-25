from django import forms
from django.contrib.auth.models import User
from .models import Donor, Patient, BloodStock, BloodDonation, BloodRequest

# Donor Signup Form
class DonorSignupForm(forms.ModelForm):
    username = forms.CharField(max_length=150, label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    name = forms.CharField(max_length=100, label="Full Name")

    class Meta:
        model = Donor
        fields = ['name', 'blood_group', 'contact_number', 'address']
        widgets = {
            'blood_group': forms.Select(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def save(self, commit=True):
        # Create the User object first
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password']
        )
        donor = super().save(commit=False)
        donor.user = user
        if commit:
            donor.save()
        return donor

# Patient Signup Form
class PatientSignupForm(forms.ModelForm):
    username = forms.CharField(max_length=150, label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    name = forms.CharField(max_length=100, label="Full Name")

    class Meta:
        model = Patient
        fields = ['name', 'blood_group', 'contact_number', 'address']
        widgets = {
            'blood_group': forms.Select(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def save(self, commit=True):
        # Create the User object first
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password']
        )
        patient = super().save(commit=False)
        patient.user = user
        if commit:
            patient.save()
        return patient

# Blood Stock Form
class BloodStockForm(forms.ModelForm):
    class Meta:
        model = BloodStock
        fields = ['blood_group', 'units']
        widgets = {
            'blood_group': forms.Select(attrs={'class': 'form-control'}),
            'units': forms.NumberInput(attrs={'min': 0, 'class': 'form-control'}),
        }

# Blood Donation Form
class BloodDonationForm(forms.ModelForm):
    class Meta:
        model = BloodDonation
        fields = ['units_donated']
        widgets = {
            'units_donated': forms.NumberInput(attrs={'min': 1, 'max': 5, 'class': 'form-control'}),
        }


# Blood Request Form
class BloodRequestForm(forms.ModelForm):
    class Meta:
        model = BloodRequest
        fields = ['blood_group', 'units_requested']
        widgets = {
            'blood_group': forms.Select(attrs={'class': 'form-control'}),
            'units_requested': forms.NumberInput(attrs={'min': 1, 'max': 5, 'class': 'form-control'}),
        }
