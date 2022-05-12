from django.dispatch import receiver
from django.db.models.signals import post_delete

from .models import Chercheur, Thesard, Professeur, DirecteurLabo

@receiver(post_delete, sender=Chercheur)
def chercheurDeleted(sender, instance, **kwargs):
    instance.utilisateur.delete()

@receiver(post_delete, sender=Thesard)
def thesardDeleted(sender, instance, **kwargs):
    instance.chercheur.utilisateur.delete()

@receiver(post_delete, sender=Professeur)
def professeurDeleted(sender, instance, **kwargs):
    instance.chercheur.utilisateur.delete()

@receiver(post_delete, sender=DirecteurLabo)
def directeurLaboDeleted(sender, instance, **kwargs):
    instance.chercheur.utilisateur.delete()
