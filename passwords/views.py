from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from .models import Password
from .forms import PasswordForm
import random
import string


def register(request): # регистрация
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('password_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'passwords/register.html', {'form': form})


def login_view(request): # вход
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
def password_list(request): # отображение паролей
    user_passwords = Password.objects.filter(user=request.user)
    return render(request, 'passwords/password_list.html', {'passwords': user_passwords})


@login_required
def password_add(request): # добавление пароля
    if request.method == 'POST':
        form = PasswordForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('password_list')
    else:
        form = PasswordForm(user=request.user)

    return render(request, 'passwords/password_form.html', {'form': form})


def generate_random_password(length=12): # генерация случайного пароля
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))


@login_required
def generate_random_password_view(request): # генерация случайного пароля
    random_password = generate_random_password()

    if request.method == 'POST':
        form = PasswordForm(request.POST, user=request.user)
        if form.is_valid():
            password_entry = form.save(commit=False)
            password_entry.password = random_password
            password_entry.save()
            return redirect('password_list')
    else:
        form = PasswordForm(user=request.user)

    return render(request, 'passwords/password_form.html', {'form': form, 'generated_password': random_password})


@login_required
def password_edit(request, password_id): # редактирование пароля
    password = Password.objects.get(id=password_id, user=request.user)

    if request.method == 'POST':
        form = PasswordForm(request.POST, instance=password)
        if form.is_valid():
            form.save()
            return redirect('password_list')
    else:
        form = PasswordForm(instance=password)

    return render(request, 'passwords/password_form.html', {'form': form})


@login_required
def password_delete(request, password_id): # удаление пароля
    password = Password.objects.get(id=password_id, user=request.user)

    if request.method == 'POST':
        password.delete()
        return redirect('password_list')

    return render(request, 'passwords/password_delete.html', {'password': password})
