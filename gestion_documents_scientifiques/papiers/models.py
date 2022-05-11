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
    titre = models.CharField("Titre", max_length=200, null=False, blank=False)
    indexation = models.CharField("Indexation", max_length=50, choices=Index.choices, null=False, blank=False)
    est_valide = models.BooleanField(default=False, editable=False)

class PublicationRevueInternational(Papier):
    nomJournal = models.CharField("Nom Du Journal", max_length=200, null=False, blank=False)
    numeroJournal = models.PositiveIntegerField("Numéro Du Journal", null=False, blank=False)
    volumeJournal = models.PositiveIntegerField("Volume", null=False, blank=False)
    anneePublication = models.PositiveSmallIntegerField("Année de Publication", null=False, blank=False)
    pageDébut = models.PositiveIntegerField("Page de Début", null=False, blank=False)
    pageFin = models.PositiveIntegerField("Page de Fin", null=False, blank=False)
