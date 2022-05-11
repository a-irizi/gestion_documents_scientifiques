from django.dispatch import receiver
from django.db.models.signals import post_delete

from .models import Thesard, Professeur, DirecteurLabo

@receiver(post_delete, sender=Thesard)
def thesardDeleted(sender, instance, **kwargs):
    instance.utilisateur.delete()

@receiver(post_delete, sender=Professeur)
def thesardDeleted(sender, instance, **kwargs):
    instance.utilisateur.delete()

@receiver(post_delete, sender=DirecteurLabo)
def thesardDeleted(sender, instance, **kwargs):
    instance.utilisateur.delete()
