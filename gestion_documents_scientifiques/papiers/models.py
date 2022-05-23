import uuid
from django.db import models

# Create your models here.
class Papier(models.Model):
    class Index(models.TextChoices):
        SCOPUS = "SCOPUS", "Scopus"
        WEB_OF_SCIENCE = "WEB_OF_SCIENCE", "Web Of Science"
        AUTRE = "AUTRE", "Autre"
        AUCUNE = "AUCUNE", "Aucune"
    class PapierType(models.TextChoices):
        PUBLICATION_REVUE_INTERNATIONAL = 'PUBLICATION REVUE INTERNATIONAL', 'Publication Revue International'
        CHAPITRE_OUVRAGE = 'CHAPITRE OUVRAGE', 'Chapitre Ouvrage'
        COMMUNICATION_INTERNATIONAL = 'COMMUNICATION INTERNATIONAL', 'Communication International'
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    titre = models.CharField("Titre", max_length=200, null=False, blank=False)
    indexation = models.CharField("Indexation", max_length=50, choices=Index.choices, null=False, blank=False)
    est_valide = models.BooleanField(default=False, editable=False)
    papier = models.FileField("Papier", upload_to='files/')
    papierType = models.CharField("Type", max_length=50, choices=PapierType.choices, null=False, blank=False)
    def __str__(self):
        return self.titre

class PublicationRevueInternational(Papier):
    nomJournal = models.CharField("Nom Du Journal", max_length=200, null=False, blank=False)
    numeroJournal = models.PositiveIntegerField("Numéro Du Journal", null=False, blank=False)
    volumeJournal = models.PositiveIntegerField("Volume", null=False, blank=False)
    anneePublication = models.PositiveSmallIntegerField("Année de Publication", null=False, blank=False)
    pageDébut = models.PositiveIntegerField("Page de Début", null=False, blank=False)
    pageFin = models.PositiveIntegerField("Page de Fin", null=False, blank=False)


class ChapitreOuvrage(Papier):
    nomOuvrage = models.CharField("Nom d'Ouvrage", max_length=200, null=False, blank=False)
    EditionOuvrage = models.PositiveIntegerField("Edition d'Ouvrage", null=False, blank=False)
    nomChapitre = models.CharField("Nom du Chapitre", max_length=200, null=False, blank=False)
    datePublication = models.DateField("Date de Publication", null=False, blank=False)
    pageDébut = models.PositiveIntegerField("Page de Début", null=False, blank=False)
    pageFin = models.PositiveIntegerField("Page de Fin", null=False, blank=False)

class CommunicationInternational(Papier):
    class CommunicationInternationalType(models.TextChoices):
        WORKSHOP = "WORKSHOP", "Workshop"
        CONFERENCE = "CONFERENCE", "Conference"
        AUTRE = "AUTRE", "Autre"

    nomConférence = models.CharField("Nom du Conférence", max_length=200, null=False, blank=False)
    ville = models.CharField("Ville", max_length=200, null=False, blank=False)
    pays = models.CharField("Pays", max_length=200, null=False, blank=False)
    date = models.DateField("Date du Conférence", null=False, blank=False)
    pageDébut = models.PositiveIntegerField("Page de Début", null=False, blank=False)
    pageFin = models.PositiveIntegerField("Page de Fin", null=False, blank=False)
    communication = models.FileField("Communication", upload_to='files/')
    communicationInternationalType = models.CharField("Type De Communication", max_length=50, choices=CommunicationInternationalType.choices, null=False, blank=False)