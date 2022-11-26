from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from django.views.generic import CreateView

from users.forms import RegisterUserForm


# Create your views here.

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = "login.html"
    success_url = reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('home')


def user_profile(request):
    return render(request, "profile.html")


def successful(request):
    return render(request, "successful.html")
