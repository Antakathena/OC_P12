from django.db import transaction

from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager
)


class CustomUserManager(BaseUserManager):

    def create(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email,and password.
        """
        return self._create_user(email, password=password, **extra_fields)

    def _create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email,and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        try:
            with transaction.atomic():  # on essaye avec si ça plante, retirer
                user = self.model(email=email, **extra_fields)  # self.normalize_email(email)
                user.set_password(password)
                user.is_staff = True if user.team == "management" else False  # on essaie
                user.save(using=self._db)
                return user
        except Exception as e:
            print(e)
            raise e

    def create_user(self, email, password=None, **extra_fields):
        # extra_fields.setdefault('is_staff', False)  # retiré pour faire echo à l.28 ajoutée
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password=password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(email, password=password, **extra_fields)
