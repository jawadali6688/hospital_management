from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login  # ✅ Fix: Importing missing authentication methods
from django.contrib.auth.models import User, Group
from django.utils.timezone import now, timedelta
from .models import TemporaryRole
from users.decorators import role_required


def home(request):
    return render(request, 'home.html')  # Yeh ek simple template render karega


# ✅ Assign Temporary Role (Only Super Admin Can Assign)
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
        user.groups.add(role)  # ✅ Role assign

        messages.success(request, f"{user.username} assigned {role.name} for {duration_hours} hours!")
        return redirect("dashboard")

    users = User.objects.exclude(is_superuser=True)
    roles = Group.objects.all()
    return render(request, "users/assign_temporary_role.html", {"users": users, "roles": roles})

# ✅ General Dashboard View (Accessible by All Logged-in Users)
@login_required
def dashboard_view(request):
    return render(request, 'users/dashboard.html')

# ✅ Doctor Dashboard (Only Doctors Allowed)
@login_required
@role_required(allowed_roles=['doctor'])  # ✅ Fix: Apply role check
def doctor_dashboard(request):
    return render(request, 'users/doctor_dashboard.html')

# ✅ Patient Dashboard (Only Patients Allowed)
@login_required
@role_required(allowed_roles=['patient'])  # ✅ Fix: Apply role check
def patient_dashboard(request):
    return render(request, 'users/patient_dashboard.html')

# ✅ Guardian Dashboard (Only Guardians Allowed)
@login_required
@role_required(allowed_roles=['guardian'])  # ✅ Fix: Apply role check
def guardian_dashboard(request):
    return render(request, 'users/guardian_dashboard.html')


@login_required
def dashboard_redirect(request):
    if request.user.is_superuser:
        return redirect("/admin")
    
    role_redirects = {
        'super_admin': '/admin/accounts/',
        'doctor': '/doctor-dashboard/',
        'patient': '/patient-dashboard/',
        'guardian': '/guardian-dashboard/',
    }
    return redirect(role_redirects.get(request.user.role, '/'))

# ✅ User Login View
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")

        else:
            messages.error(request, "Invalid username or password")

    return render(request, "users/login.html")

# ✅ User Registration View
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])  # ✅ Password hashing
            user.save()
            messages.success(request, "Your account has been created! You can now log in.")
            return redirect("login")  # ✅ Redirect to login page
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserRegisterForm()

    return render(request, "users/signup.html", {"form": form})
