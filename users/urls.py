# # from django.urls import path
# from django.contrib.auth import views as auth_views
# from . import views  # ✅ Yeh sari views ek saath import kar raha hai

# urlpatterns = [
#     path("register/", views.register, name="register"),
#     path("dashboard/", views.dashboard_view, name="dashboard"),
#     path("assign_temporary_role/", views.assign_temporary_role, name="assign_temporary_role"),
#     path("doctor/dashboard/", views.doctor_dashboard, name="doctor_dashboard"),
#     path("patient/dashboard/", views.patient_dashboard, name="patient_dashboard"),
#     path("guardian/dashboard/", views.guardian_dashboard, name="guardian_dashboard"),

#     # Authentication URLs
#     path("login/", auth_views.LoginView.as_view(template_name="users/login.html"), name="login"),
#     path("logout/", auth_views.LogoutView.as_view(), name="logout"),
#     path("password_change/", auth_views.PasswordChangeView.as_view(template_name="users/password_change.html"), name="password_change"),
#     path("password_change/done/", auth_views.PasswordChangeDoneView.as_view(template_name="users/password_change_done.html"), name="password_change_done"),
#     path("password_reset/", auth_views.PasswordResetView.as_view(template_name="users/password_reset.html"), name="password_reset"),
#     path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"), name="password_reset_done"),
#     path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="users/password_reset_confirm.html"), name="password_reset_confirm"),
#     path("reset/done/", auth_views.PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"), name="password_reset_complete"),
# ]
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views  # ✅ Yeh sari views ek saath import kar raha hai

urlpatterns = [
    path("register/", views.register, name="register"),
    path("accounts/", views.dashboard_redirect, name="dashboard_redirect"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("assign_temporary_role/", views.assign_temporary_role, name="assign_temporary_role"),
    path("doctor/dashboard/", views.doctor_dashboard, name="doctor_dashboard"),
    path("patient/dashboard/", views.patient_dashboard, name="patient_dashboard"),
    path("guardian/dashboard/", views.guardian_dashboard, name="guardian_dashboard"),

    # Authentication URLs
    path("login/", auth_views.LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("password_change/", auth_views.PasswordChangeView.as_view(template_name="users/password_change.html"), name="password_change"),
    path("password_change/done/", auth_views.PasswordChangeDoneView.as_view(template_name="users/password_change_done.html"), name="password_change_done"),
    path("password_reset/", auth_views.PasswordResetView.as_view(template_name="users/password_reset.html"), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="users/password_reset_confirm.html"), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"), name="password_reset_complete"),
]
