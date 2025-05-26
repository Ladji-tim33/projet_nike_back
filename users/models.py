from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True)  # S'assurer qu'il est unique

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # Ce champ reste obligatoire pour l’admin

    def __str__(self):
        return self.email
