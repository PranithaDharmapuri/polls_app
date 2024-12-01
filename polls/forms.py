from django import forms

class NameForm(forms.Form):
    your_name=forms.CharField(label="Your name", max_length=100)
    email=forms.CharField(label="Email",max_length=100)
    password=forms.CharField(label="password",max_length=6)