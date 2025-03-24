from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Password


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class PasswordForm(forms.ModelForm):
    class Meta:
        model = Password
        fields = ['site', 'username', 'password']

    def save(self, commit=True):
        password = super().save(commit=False)
        password.user = self.instance.user  # привязываем к текущему пользователю
        if commit:
            password.save()
        return password