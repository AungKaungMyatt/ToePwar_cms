from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('super_admin', 'Super Admin'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='admin')