import logging

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser


class UserManager(BaseUserManager):
    logger = logging.getLogger(__name__)

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

    def create_superuser(self, username, role='gestion', password=None, **extra_fields):
        print("superuser")
        try:
            user = self.get(username=username)
        except self.model.DoesNotExist:
            user = self.create_user(
                username=username,
                role=role,
                password=password,
                **extra_fields
            )
        else:
            user.role = role
            user.set_password(password)
            for key, value in extra_fields.items():
                setattr(user, key, value)
            user.save()

        user.is_staff = True
        user.is_superuser = True
        user.save()

        return user


class User(AbstractUser):
    """Classe contenant tous les champs et méthodes de User par défaut.
    Args:
        AbstractUser (class): classe par défaut django pour un user
    """
    objects = UserManager()

    ROLE_CHOICES = (
        ('vente', 'Vente'),
        ('support', 'Support'),
        ('gestion', 'Gestion'),
    )

    username = models.CharField(max_length=25, primary_key=True, unique=True)
    role = models.CharField(max_length=10, blank=False, choices=ROLE_CHOICES, error_messages={
        'invalid_choice': 'Le rôle choisi est invalide. Les rôles disponibles sont : {}'.format(
            [choice[1] for choice in ROLE_CHOICES])})

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def assign_role(self):
        if self.groups.exists():
            group = self.groups.first()
            self.role = group.name
            self.save()


