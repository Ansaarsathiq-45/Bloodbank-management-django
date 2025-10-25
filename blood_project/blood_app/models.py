from django.db import models
from django.contrib.auth.models import User
from datetime import date, timedelta

# Blood group choices

BLOOD_GROUP_CHOICES = [
    ('A+', 'A+'), ('A-', 'A-'),
    ('B+', 'B+'), ('B-', 'B-'),
    ('AB+', 'AB+'), ('AB-', 'AB-'),
    ('O+', 'O+'), ('O-', 'O-'),
]


# Donor Model
class Donor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    contact_number = models.CharField(max_length=15)
    address = models.TextField()
    is_approved = models.BooleanField(default=False)  # Admin approval

    def __str__(self):
        return f"{self.name} ({self.blood_group})"

# Patient Model
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    contact_number = models.CharField(max_length=15)
    address = models.TextField()
    is_approved = models.BooleanField(default=False)  # Admin approval

    def __str__(self):
        return f"{self.name} ({self.blood_group})"

# Blood Stock Model
class BloodStock(models.Model):
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, unique=True)
    units = models.PositiveIntegerField(default=0)  # Number of units available

    def __str__(self):
        return f"{self.blood_group} - {self.units} units"


# Blood Donation Model
class BloodDonation(models.Model):
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    units_donated = models.PositiveIntegerField()
    date_donated = models.DateField(auto_now_add=True)  # Explicit date field

    def __str__(self):
        return f"{self.donor.name} donated {self.units_donated} units ({self.blood_group})"

    @staticmethod
    def can_donate(donor):
        """
        Returns True if the donor can donate again (after 90 days since last donation).
        """
        last_donation = BloodDonation.objects.filter(donor=donor).order_by('-date_donated').first()
        if not last_donation:
            return True  # First-time donor
        return (date.today() - last_donation.date_donated) >= timedelta(days=90)

# Blood Request Model
class BloodRequest(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    units_requested = models.PositiveIntegerField()
    date_requested = models.DateField(auto_now_add=True)  # Explicit date field
    status = models.CharField(
        max_length=20,
        choices=[("Pending", "Pending"), ("Approved", "Approved"), ("Rejected", "Rejected")],
        default="Pending"
    )

    def __str__(self):
        return f"{self.patient.name} requested {self.units_requested} units ({self.blood_group})"
