from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


class UserManager(BaseUserManager):
    def create_user(self, username, role, password=None, **extra_fields):
        if not role:
            raise ValueError('Users must have a role')

        user = self.model(
            username=username,
            role=role,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, role='Gestion',  password=None):
        user = self.create_user(
            username,
            role,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()
        return user


class User(AbstractUser):
    """Classe contenant tous les champs et méthodes de User par défaut.
    Args:
        AbstractUser (class): classe par défaut django pour un user
    """

    ROLE_CHOICES = (
        ('vente', 'Vente'),
        ('support', 'Support'),
    )

    username = models.CharField(max_length=25, primary_key=True, unique=True)
    role = models.CharField(max_length=10, blank=False, choices=ROLE_CHOICES, error_messages={
        'invalid_choice': 'Le rôle choisi est invalide. Les rôles disponibles sont : {}'.format([choice[1] for choice in ROLE_CHOICES])})

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def clean(self):
        super().clean()
        choices = dict(self.ROLE_CHOICES)
        if self.role not in choices:
            choices = ", ".join([choice[0] for choice in self.ROLE_CHOICES])
            raise ValidationError('Le rôle choisi est invalide. Les rôles disponibles sont : {}'.format(choices))

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username