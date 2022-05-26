from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, PermissionsMixin, UserManager

from users.managers import CustomUserManager


class CustomUser(AbstractUser, PermissionsMixin):
    """
    Les champs par défaut sont :
    id, password, last_login, is_superuser, username, fist_name,
    last_name, email, is_staff, is_active, date_joined, groups, user_permissions
    """
    TEAM_CHOICES = (
        ("management", 'management'),
        ("sales", 'sales'),
        ("support", 'support')
    )
    team = models.CharField(max_length=10, choices=TEAM_CHOICES, default="management")

    email = models.EmailField(max_length=40, unique=True)
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30)  # il faut choisir : blank = True ou required field?
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()
    # objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['team', 'first_name', 'last_name', 'username']

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.capitalize()
        self.last_name = self.last_name.upper()
        self.username = self.username.capitalize()
        super().save(*args, **kwargs)
        return self

    def __str__(self):
        return f"{self.username}, {self.team} (id:{self.id})"
