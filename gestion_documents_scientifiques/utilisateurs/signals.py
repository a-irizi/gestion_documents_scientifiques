from django.dispatch import receiver
from django.db.models.signals import post_delete

from .models import Thesard

@receiver(post_delete, sender=Thesard)
def thesardDeleted(sender, instance, **kwargs):
    instance.utilisateur.delete()