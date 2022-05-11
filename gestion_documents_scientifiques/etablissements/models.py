import uuid
from django.db import models

# Create your models here.
class Universite(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    nom = models.CharField("Nom d'Université", max_length=200, null=False, blank=False)

    def __str__(self) -> str:
        return self.nom

class Faculte(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    universite = models.ForeignKey(to=Universite, null=True, on_delete=models.SET_NULL)
    nom = models.CharField("Nom de la Faculté", max_length=200, null=False, blank=False)

    def __str__(self) -> str:
        return self.nom

class Departement(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    faculte = models.ForeignKey(to=Faculte, null=True, on_delete=models.SET_NULL)
    nom = models.CharField("Nom de Département", max_length=200, null=False, blank=False)

    def __str__(self) -> str:
        return self.nom
