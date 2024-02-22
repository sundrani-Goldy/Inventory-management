from django.contrib.auth.models import AbstractUser
from django.db import models


class NewUser(AbstractUser):
    type = models.CharField(max_length=100)

    