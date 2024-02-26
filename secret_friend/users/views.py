import uuid
from datetime import timedelta
from django.utils.timezone import now

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, TemplateView, CreateView

from .forms import LoginUserForm, RegistrationUserForm, GeneralInfoForm, CreatingWishForm
from .models import User, Wish, EmailVerification


class ProfileView(DetailView):
    model = User
    template_name = ('users/profile.html')

    def get_context_data(self, **kwargs):
        user_instance = self.get_object()
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['form'] = GeneralInfoForm(instance=self.object)
        context['wish_form'] = CreatingWishForm()
        context['my_wishes'] = Wish.objects.filter(parent=user_instance)
        return context

    def post(self, request, *args, **kwargs):
        if 'general_info' in request.POST:
            user_instance = User.objects.get(pk=self.kwargs['pk'])
            form = GeneralInfoForm(request.POST, instance=user_instance)
            if form.is_valid():
                form.save()
                return redirect(request.path)
            return super(ProfileView, self).post(request, *args, **kwargs)

        if 'creating_wish' in request.POST:
            wish_form = CreatingWishForm(request.POST)
            if wish_form.is_valid():
                parent_id = request.POST.get('user_id')
                wish = wish_form.save(commit=False)
                wish.parent_id = parent_id
                wish.save()
                return redirect(request.path)
            return super(ProfileView, self).post(request, *args, **kwargs)


class UserRegistrationView(CreateView):
    model = User
    form_class = RegistrationUserForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('rooms:AllRooms')

class EmailVerificationView(TemplateView):
    template_name = 'users/verified.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verification = EmailVerification.objects.filter(user=user, code=code)
        if email_verification.exists() and not email_verification.first().is_expired():
            user.is_verified = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('homepage'))

def logout_view(request):
    logout(request)
    return redirect('homepage')


def login_view(request):
    form = LoginUserForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('/')
    return render(request, 'users/login.html', {'form': form})


