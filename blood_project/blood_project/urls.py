"""
URL configuration for blood_project project.

The `urlpatterns` list routes URLs to views.
"""
from django.contrib import admin
from django.urls import path
from blood_app.views import (
    home,
    donor_signup,
    donor_login,
    patient_signup,
    patient_login,
    user_logout,
    manage_blood_stock,
    dashboard,
    donate_blood,
    blood_request_view,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('donor/signup/', donor_signup, name='donor_signup'),
    path('donor/login/', donor_login, name='donor_login'),
    path('patient/signup/', patient_signup, name='patient_signup'),
    path('patient/login/', patient_login, name='patient_login'),
    path('logout/', user_logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('blood/manage/', manage_blood_stock, name='manage_blood_stock'),
    path('donate/', donate_blood, name='donate_blood'),
    path('request/', blood_request_view, name='blood_request'),
]
