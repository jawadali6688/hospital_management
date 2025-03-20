from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login  
from django.contrib.auth.models import User, Group
from django.utils.timezone import now, timedelta
from .models import TemporaryRole, Patient, Doctor
from users.decorators import role_required


def home(request):
    return render(request, 'home.html')


# Assign Temporary Role (Only Super Admin Can Assign)
def assign_temporary_role(request):
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to assign temporary roles.")
        return redirect("dashboard")

    if request.method == "POST":
        user_id = request.POST.get("user_id")
        role_id = request.POST.get("role_id")
        duration_hours = int(request.POST.get("duration", 1))  # Default: 1 hour
        
        user = User.objects.get(id=user_id)
        role = Group.objects.get(id=role_id)
        duration = timedelta(hours=duration_hours)

        temp_role = TemporaryRole.objects.create(
            user=user,
            role=role,
            assigned_by=request.user,
            duration=duration,
            expires_at=now() + duration
        )
        user.groups.add(role)  # Assign Role

        messages.success(request, f"{user.username} assigned {role.name} for {duration_hours} hours!")
        return redirect("dashboard")

    users = User.objects.exclude(is_superuser=True)
    roles = Group.objects.all()
    return render(request, "users/assign_temporary_role.html", {"users": users, "roles": roles})


# General Dashboard View (Accessible by All Logged-in Users)
@login_required
def dashboard_view(request):
    return render(request, 'users/dashboard.html')


# Doctor Dashboard (Only Doctors Allowed)
@login_required
@role_required(allowed_roles=['doctor'])
def doctor_dashboard(request):
    if request.user.role != 'doctor':
        return HttpResponseForbidden("searching....")

    # Iss doctor ke assigned patients
    patients = Patient.objects.filter(assigned_doctor=request.user.doctor_profile)

    return render(request, 'users/doctor_dashboard.html', {'patients': patients})


# Patient Dashboard (Only Patients Allowed)
@login_required
@role_required(allowed_roles=['patient'])
def patient_dashboard(request):
     if request.user.role != 'patient':
        return HttpResponseForbidden("page reload.")

 
     return render(request, 'users/patient_dashboard.html')


# Guardian Dashboard (Only Guardians Allowed)
@login_required
@role_required(allowed_roles=['guardian'])
def guardian_dashboard(request):
    return render(request, 'users/guardian_dashboard.html')


# View Patient History (For Doctors, Guardians, Admins, Super Admins)
@login_required
def view_patient_history(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if (
        request.user == patient.assigned_doctor.user
        or hasattr(request.user, 'guardian_profile')  # Guardian access
        or request.user.role in ['admin', 'super_admin']  # Admin & Super Admin access
    ):
        return render(request, 'users/view_patient_history.html', {'patient': patient})
    
    return render(request, '403.html')
    #  Access Control: Only Allowed Roles Can View
    # if not (
    #     request.user.is_superuser or
    #     request.user.role == "admin" or
    #     (request.user.role == "doctor" and patient.assigned_doctor.user == request.user) or
    #     (request.user.role == "guardian" and request.user.guardian_profile == patient.user.guardian_profile)
    # ):
    #     return HttpResponseForbidden("You do not have permission to view this patient's history.")

    # return render(request, "users/patient_history.html", {"patient": patient})


@login_required
def dashboard_redirect(request):
    if request.user.is_superuser:
        return redirect("/admin")
    
    
    role_redirects = {
        'super_admin': '/admin/accounts/',
        'doctor': '/doctor/dashboard/',
        'patient': '/patient/dashboard/',
        'guardian': '/guardian/dashboard/',
    }
    return redirect(role_redirects.get(request.user.role, '/'))


# User Login View
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            
            # ✅ Redirect based on role
            role_redirects = {
                'super_admin': '/admin/accounts/',
                'doctor': '/doctor/dashboard/',
                'patient': '/patient/dashboard/',
                'guardian': '/guardian/dashboard/',
            }
            
            return redirect(role_redirects.get(user.role, '/'))  # ✅ Correct role-based redirect

        else:
            messages.error(request, "Invalid username or password")

    return render(request, "users/login.html")


# User Registration View
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])  # Password hashing
            user.save()
            messages.success(request, "Your account has been created! You can now log in.")
            return redirect("login")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserRegisterForm()

    return render(request, "users/signup.html", {"form": form})
