from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.conf import settings
from django.utils.timezone import now

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('', 'No Role'),  # ✅ Super Admin ke liye empty role
        ('admin', 'Admin'),
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
        ('guardian', 'Guardian'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=True, default='')

    def __str__(self):
        return f"{self.username} - {self.role if self.role else 'Super Admin'}"

class Doctor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="doctor_profile")
    specialization = models.CharField(max_length=100)
    experience = models.IntegerField()
    phone = models.CharField(max_length=15)

class Patient(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="patient_profile")
    medical_history = models.TextField()
    assigned_doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)

class Guardian(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="guardian_profile")
    phone = models.CharField(max_length=15)

class TemporaryRole(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.ForeignKey(Group, on_delete=models.CASCADE)  
    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="assigned_roles", on_delete=models.CASCADE
    )

    start_time = models.DateTimeField(default=now)
    duration = models.DurationField()
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = self.start_time + self.duration
        super().save(*args, **kwargs)

    def is_expired(self):
        return now() >= self.expires_at

    def __str__(self):
        return f"{self.user} as {self.role} (Expires: {self.expires_at})"

def assign_permissions(user):
    """✅ Optimized function to assign group permissions."""
    if user.groups.exists():
        return  # ✅ Agar user already kisi group me hai to dobara assign na karein

    role_group_map = {
        "admin": "Admin",
        "doctor": "Doctor",
        "patient": "Patient",
        "guardian": "Guardian",
    }

    role = user.role.lower()
    if role in role_group_map:
        group, _ = Group.objects.get_or_create(name=role_group_map[role])
        user.groups.add(group)
