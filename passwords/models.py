from django.db import models
from django.contrib.auth.models import User


class Password(models.Model):
    site = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="passwords")

    def __str__(self):
        return self.site

    class Meta:
        ordering = ["site"]