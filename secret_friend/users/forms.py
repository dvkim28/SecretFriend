from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django import forms

class LoginUserForm(forms.Form):
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username',
    }))
    password = forms.CharField(label="password", widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username',
    }))

    def clean(self, *args, **kwargs):
        cleaned_data = super().clean()
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError('Username and password do not match')
        return cleaned_data

class RegistrationUserForm(forms.ModelForm):
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username',
    }))
    password = forms.CharField(label="password", widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username',
    }))
    password1 = forms.CharField(label="password", widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username',
    }))
    class Meta:
        model = User
        fields = ['username',]

    def clean_password1(self):
        data = self.cleaned_data
        if data['password'] != data['password1']:
            raise forms.ValidationError('Password must be the same')
        return data['password']




