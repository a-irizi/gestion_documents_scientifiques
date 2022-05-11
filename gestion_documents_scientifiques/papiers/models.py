import uuid
from django.db import models

# Create your models here.
class Papier(models.Model):
    class Index(models.TextChoices):
        SCOPUS = "SCOPUS", "Scopus"
        WEB_OF_SCIENCE = "WEB_OF_SCIENCE", "Web Of Science"
        AUTRE = "AUTRE", "Autre"
        AUCUNE = "AUCUNE", "Aucune"
    id = models.UUIDField(uuid.uuid4, editable=False, primary_key=True)
    titre = models.CharField(max_length=200, null=False, blank=False)
    indexation = models.CharField(max_length=50, choices=Index.choices, null=False, blank=False)
    est_valide = models.BooleanField(default=False, editable=False)
