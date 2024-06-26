from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    User entity.
    """
    email = models.EmailField(unique=True)
