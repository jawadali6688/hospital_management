"""
URL configuration for hospital_portal2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
# from django.urls import path, include
# from users import views  # Users ke views ko import kar rahe hain

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('users/', include('users.urls')),  # ✅ Ensure karo users/urls.py properly set ho
#     path("register/", views.register, name="register"),
#     path('dashboard/', views.dashboard_view, name='dashboard'),
#     path("assign_temporary_role/", views.assign_temporary_role, name="assign_temporary_role"),
#     path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
#     path('patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),
#     path('guardian/dashboard/', views.guardian_dashboard, name='guardian_dashboard'),
# ]
from django.contrib import admin
from django.urls import path, include  #  `include` ka sahi use karo
from users.views import home  #  Home view import karein

urlpatterns = [
    path("admin/", admin.site.urls),  

    path('', home, name='home'),  #  Default homepag
    path("users/", include("users.urls")),  #  Ye line handle karegi users ke saare URLs
]
