from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError




class UserRegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            "class": "w-full px-4 py-3 border border-gray-600 rounded-lg bg-[#1E1E1E] text-gray-200  focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-orange-500  transition duration-300 ",
            "placeholder": "Enter your password"
        }),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            "class": "w-full px-4 py-3 border border-gray-600 rounded-lg bg-[#1E1E1E] text-gray-200 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-orange-500 transition duration-300 ",
            "placeholder": "Confirm your password"
        }),
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        widgets = {
            "username": forms.TextInput(attrs={
                "class": "w-full px-4 py-3 border border-gray-600 rounded-lg bg-[#1E1E1E] text-gray-200 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-orange-500  transition duration-300 ",
                "placeholder": "Enter your username"
            }),
            "email": forms.EmailInput(attrs={
                "class": "w-full px-4 py-3 border border-gray-600 rounded-lg bg-[#1E1E1E] text-gray-200 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-orange-500  transition duration-300 ",
                "placeholder": "Enter your email"
            }),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already in use.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match.")

        return cleaned_data
