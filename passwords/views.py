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
    return render(request, 'registration/register.html', {'form': form})


def password_list(request):
    user_passwords = Password.objects.filter(user=request.user)
    return render(request, 'passwords/password_list.html', {'passwords': user_passwords})


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


def generate_random_password_view(request):
    random_password = generate_random_password()
    form = PasswordForm({'password': random_password})
    if form.is_valid():
        form.save()
        return redirect('password_list')
    return render(request, 'passwords/password_form.html', {'form': form})