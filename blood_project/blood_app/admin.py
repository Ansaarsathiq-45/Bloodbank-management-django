from django.contrib import admin
from .models import Donor, Patient, BloodStock

# Action to approve selected users
def approve_users(modeladmin, request, queryset):
    queryset.update(is_approved=True)
    modeladmin.message_user(request, "Selected users have been approved successfully.")
approve_users.short_description = "Approve selected users"

# Donor Admin
@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'blood_group', 'contact_number', 'is_approved')
    list_editable = ('is_approved',)
    search_fields = ('name', 'user__username', 'blood_group')
    actions = [approve_users]  # Add custom action

# Patient Admin
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'blood_group', 'contact_number', 'is_approved')
    list_editable = ('is_approved',)
    search_fields = ('name', 'user__username', 'blood_group')
    actions = [approve_users]  # Add custom action

# Blood Stock Admin
@admin.register(BloodStock)
class BloodStockAdmin(admin.ModelAdmin):
    list_display = ('blood_group', 'units')
    search_fields = ('blood_group',)
