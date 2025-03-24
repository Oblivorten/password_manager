from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from .models import Password
from .forms import PasswordForm
import random
import string


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'passwords/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('password_list')
        else:
            return render(request, 'passwords/login.html', {'form': form, 'error_messages': form.errors})
    else:
        form = AuthenticationForm()
    return render(request, 'passwords/login.html', {'form': form})


@login_required
def password_list(request):
    user_passwords = Password.objects.filter(user=request.user)
    return render(request, 'passwords/password_list.html', {'passwords': user_passwords})


@login_required()
def password_add(request):
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('password_list')
    else:
        form = PasswordForm()
    return render(request, 'passwords/password_form.html', {'form': form})


def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))


@login_required()
def generate_random_password_view(request):
    random_password = generate_random_password()
    form = PasswordForm({'password': random_password})
    if form.is_valid():
        form.save()
        return redirect('password_list')
    return render(request, 'passwords/password_form.html', {'form': form})