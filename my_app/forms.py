from typing import Any
from django import forms
from .models import User

class LoginForm(forms.Form):
    name=forms.CharField(label="name",max_length=150)
    email=forms.EmailField(label="Email",max_length=200)
    password=forms.CharField(label="Password",widget=forms.PasswordInput)

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields=['name','email','password']
        widgets={
            'password':forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data=super().clean()
        password=cleaned_data.get("password")

        return cleaned_data