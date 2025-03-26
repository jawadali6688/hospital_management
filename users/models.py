# from django.contrib.auth.models import AbstractUser, Group
# from django.db import models
# from django.conf import settings
# from django.utils.timezone import now

# class CustomUser(AbstractUser):
#     ROLE_CHOICES = [
#         ('', 'No Role'),  #  Super Admin ke liye empty role
#         ('admin', 'Admin'),
#         ('doctor', 'Doctor'),
#         ('patient', 'Patient'),
#         ('guardian', 'Guardian'),
#     ]
    
#     role = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=True, default='')
#     def save(self, *args, **kwargs):
#         is_new = self._state.adding  # ✅ Check if this is a new user being created
#         super().save(*args, **kwargs)  # ✅ Pehle user ko save karo

#         if is_new:  # ✅ Agar naya user hai to related table me bhi entry save karo
#             if self.role == "doctor":
#                 Doctor.objects.create(user=self)
#             elif self.role == "patient":
#                 Patient.objects.create(user=self)
#             elif self.role == "guardian":
#                 Guardian.objects.create(user=self)
#     def __str__(self):
#         return f"{self.username} - {self.role if self.role else 'Super Admin'}"

# class Doctor(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="doctor_profile")
#     specialization = models.CharField(max_length=100)
#     experience = models.IntegerField()
#     phone = models.CharField(max_length=15)

# class Patient(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="patient_profile")
#     medical_history = models.TextField()
#     assigned_doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)

# class Guardian(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="guardian_profile")
#     phone = models.CharField(max_length=15)

# class TemporaryRole(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     role = models.ForeignKey(Group, on_delete=models.CASCADE)  
#     assigned_by = models.ForeignKey(
#         settings.AUTH_USER_MODEL, related_name="assigned_roles", on_delete=models.CASCADE
#     )

#     start_time = models.DateTimeField(default=now)
#     duration = models.DurationField()
#     expires_at = models.DateTimeField()

#     def save(self, *args, **kwargs):
#         if not self.expires_at:
#             self.expires_at = self.start_time + self.duration
#         super().save(*args, **kwargs)

#     def is_expired(self):
#         return now() >= self.expires_at

#     def __str__(self):
#         return f"{self.user} as {self.role} (Expires: {self.expires_at})"

# def assign_permissions(user):
#     """ Optimized function to assign group permissions."""
#     if user.groups.exists():
#         return  #  Agar user already kisi group me hai to dobara assign na karein

#     role_group_map = {
#         "admin": "Admin",
#         "doctor": "Doctor",
#         "patient": "Patient",
#         "guardian": "Guardian",
#     }

#     role = user.role.lower()
#     if role in role_group_map:
#         group, _ = Group.objects.get_or_create(name=role_group_map[role])
#         user.groups.add(group)
from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.conf import settings
from django.utils.timezone import now
from django.utils.crypto import get_random_string
from django.conf import settings  # Correct way to reference custom User model

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('', 'No Role'),  # Super Admin ke liye empty role
        ('admin', 'Admin'),
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
        ('guardian', 'Guardian'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=True, default='')

    def save(self, *args, **kwargs):
        is_new = self._state.adding  # Check if this is a new user being created

        # Automatically assign a username if not provided
        if not self.username:
            self.username = f"{self.role}_{get_random_string(8)}"

        # Automatically assign a password if not provided
        if not self.password:
            self.set_password(get_random_string(12))  # Generates a random secure password

        super().save(*args, **kwargs)  # Save user first

        if is_new:  # If new user, create profile in related model
            if self.role == "doctor":
                Doctor.objects.create(user=self)
            elif self.role == "patient":
                Patient.objects.create(user=self)
            elif self.role == "guardian":
                Guardian.objects.create(user=self)

        # Assign group-based permissions
        assign_permissions(self)

    def __str__(self):
        return f"{self.username} - {self.role if self.role else 'Super Admin'}"

class Doctor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="doctor_profile")
    specialization = models.CharField(max_length=100)
    experience = models.IntegerField()
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')], null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    license_number = models.CharField(max_length=50, default="TEMP-LICENSE")
    years_of_experience = models.IntegerField(default=0)
    available_days = models.CharField(max_length=255, default="Monday to Friday")

    shift_timings = models.CharField(max_length=100, default="9 AM - 5 PM")  # Default added
    assigned_patients = models.ManyToManyField('Patient', related_name="doctors", blank=True)
    status = models.CharField(max_length=20, choices=[('Active', 'Active'), ('On Leave', 'On Leave')], default='Active')


    def __str__(self):
        return f"Dr. {self.user.username} - {self.specialization}"

class Patient(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="patient_profile")
    medical_history = models.TextField()
    assigned_doctors = models.ManyToManyField(Doctor, blank=True)  # Multiple doctors allowed
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[("male", "Male"), ("female", "Female"), ("other", "Other")], null=True, blank=True)
    contact_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    blood_group = models.CharField(max_length=5, choices=[
        ("A+", "A+"), ("A-", "A-"), ("B+", "B-"), 
        ("O+", "O-"), ("AB+", "AB-")
    ], null=True, blank=True)
    
    allergies = models.TextField(null=True, blank=True)
    current_medications = models.TextField(null=True, blank=True)
    last_checkup_date = models.DateField(null=True, blank=True)
    
    emergency_contact_name = models.CharField(max_length=100, null=True, blank=True)
    emergency_contact_number = models.CharField(max_length=15, null=True, blank=True)
    emergency_contact_relation = models.CharField(max_length=50, null=True, blank=True)
    admission_date = models.DateTimeField(null=True, blank=True)
    discharge_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} (Patient)"

class Guardian(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  

    phone = models.CharField(max_length=15)
    relation = models.CharField(max_length=50, default="Unknown")  # Default value add ki
    address = models.TextField(default="Update Required")  # Temporary default
    def __str__(self):
        return self.user.username
    
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
    """ Optimized function to assign group permissions."""
    if user.groups.exists():
        return  # If user is already in a group, don't assign again

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

