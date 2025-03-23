from django.contrib import admin
from .models import Password


@admin.register(Password)
class PasswordAdmin(admin.ModelAdmin):
    list_display = ('site', 'username', 'password')
    list_filter = ('site',)
    search_fields = ('site', 'username')


