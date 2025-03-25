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

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        password = super().save(commit=False)
        if self.user:
            password.user = self.user
        if commit:
            password.save()
        return password
