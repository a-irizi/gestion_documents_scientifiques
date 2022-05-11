from django.contrib import admin

from .models import PublicationRevueInternational, ChapitreOuvrage, CommunicationInternational

# Register your models here.
admin.site.register(PublicationRevueInternational)
admin.site.register(ChapitreOuvrage)
admin.site.register(CommunicationInternational)
