from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect

from .forms import RegistrationUserForm, LoginUserForm


def registration(request):
    if request.method == 'POST':
        form = RegistrationUserForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(request.POST.get('password'))
            new_user.save()
            messages.success(request, 'Registration successful')
            return render(request, 'game/index.html', {'new_user': new_user})
        return render(request, 'users/registration.html', {'form': form})
    else:
        form = RegistrationUserForm(request.POST or None)
        return render(request, 'users/registration.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('homepage')

def login_view(request):
    form = LoginUserForm(request.POST or None)
    _next = request.GET.get('next')
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        _next = _next or '/'
        return redirect('/')
    return render(request, 'users/login.html', {'form':form})