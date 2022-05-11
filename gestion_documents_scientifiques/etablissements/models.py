import uuid
from django.db import models

# Create your models here.
class Universite(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    nom = models.CharField("Nom d'Université", max_length=200, null=False, blank=False)

    def __str__(self) -> str:
        return self.nom