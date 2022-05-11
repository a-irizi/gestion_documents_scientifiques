from django.db import models

import uuid
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

import utilisateurs

# Create your models here.


class UtilisateurManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(
        self, nom, prenom, email, password=None, **extra_fields
    ):
        if not email:
            raise ValueError("The given email must be set")
        email = BaseUserManager.normalize_email(email)
        user = self.model(
            email=email,
            nom=nom,
            prenom=prenom,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self, nom, prenom, email, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(
            nom, prenom, email, password, **extra_fields
        )

    def create_superuser(
        self, nom, prenom, email, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(
            nom, prenom, email, password, **extra_fields
        )


class Utilisateur(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        max_length=200, unique=True, null=False, blank=False)
    prenom = models.CharField(max_length=50, null=False, blank=False)
    deuxiemeNom = models.CharField(max_length=50, null=True, blank=True)
    nom = models.CharField(max_length=50, null=False, blank=False)
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, null=False, primary_key=True
    )

    is_staff = models.BooleanField(
        "staff status",
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )
    is_active = models.BooleanField(
        "active",
        default=True,
        help_text="Designates whether this user should be treated as active. " +
        "Unselect this instead of deleting accounts."
    )
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    # Don't add email to REQUIRED_FIELDS, it is automatically included
    # as USERNAME_FIELD
    REQUIRED_FIELDS = ["nom", "prenom", ]
    objects = UtilisateurManager()

    def __str__(self):
        result = None
        if self.deuxiemeNom:
            result = f"{self.prenom} {self.deuxiemeNom} {self.nom}"
        else:
            result = f"{self.prenom} {self.nom}"

        return result

class Chercheur(models.Model):
    utilisateur = models.OneToOneField(
        to=Utilisateur, on_delete=models.CASCADE)
    # universite =
    # faculté =
    # departement =
    # laboratoire =
    # papier =


class Thesard(Chercheur):
    anneeDebutDoctorat = models.PositiveIntegerField(null=False, blank=False)
    sujetThese = models.CharField(max_length=200, null=False, blank=False)
    directeurThese = models.ForeignKey(to="Professeur", on_delete=models.CASCADE)

    def __str__(self):
        return self.utilisateur.__str__()


class Professeur(Chercheur):
    
    def __str__(self):
        return "Pr. " + str(self.utilisateur)