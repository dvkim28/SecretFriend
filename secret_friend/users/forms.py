import uuid
from datetime import timedelta

from django import forms
from django.contrib.auth import authenticate
from django.utils.timezone import now

from rooms.models import Room
from users.models import User, Wish, EmailVerification


class LoginUserForm(forms.Form):
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username',
    }))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={
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
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email',
    }))
    password = forms.CharField(label="password", widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username',
    }))
    password1 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm Password',
    }))
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password1']

    def clean_password1(self):
        data = self.cleaned_data
        if data['password'] != data['password1']:
            raise forms.ValidationError('Password must be the same')
        return data['password']

    def save(self, commit=True):
        user = super(RegistrationUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.save()
        expiration = now() + timedelta(days=2)
        record = EmailVerification.objects.create(code=uuid.uuid4(), user=user, expiration=expiration)
        record.send_verification_email()
        return user


class GeneralInfoForm(forms.ModelForm):
    first_name = forms.CharField(label="First name", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username',
    }))
    last_name = forms.CharField(label="Last name", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Last name',
    }))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email address',
    }))

    class Meta:
        fields = ('first_name', 'last_name', 'email')
        model = User


class CreatingWishForm(forms.ModelForm):
    name = forms.CharField(label="Wish name", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Wish name',
    }))
    url = forms.CharField(label="Link to the wish", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Link to the wish',
    }))
    comment = forms.CharField(label="Comment", required=False, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Write comment if you want to',
    }))

    class Meta:
        fields = ('name', 'url', 'comment')
        model = Wish



