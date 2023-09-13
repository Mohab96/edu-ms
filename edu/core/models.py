from django.contrib.auth.models import AbstractUser
from django.db import models


class CoreUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    password = models.CharField(max_length=128, blank=False)
