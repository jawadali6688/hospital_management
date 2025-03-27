from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Doctor, Patient, Guardian, MedicalHistory



class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Role Information', {'fields': ('role',)}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Guardian)
admin.site.register(MedicalHistory)

