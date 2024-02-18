from django import forms
from .models import Room


class RoomCreationForm(forms.ModelForm):
    name = forms.CharField(label="Game name", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Game name',
    }))
    password = forms.CharField(label="Password",required=False, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password',
    }))
    invited_emails = forms.CharField(label="Email", widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email'
    }))

    class Meta:
        model = Room
        fields = ['name', 'password', 'invited_emails']

class PasswordForm(forms.Form):
    password = forms.CharField(label='Password', max_length=10, widget=forms.PasswordInput)
    room_id = forms.CharField(widget=forms.HiddenInput())
