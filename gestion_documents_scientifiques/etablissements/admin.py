from django.contrib import admin

from .models import Departement, Laboratoire, Universite, Faculte
# Register your models here.

admin.site.register(Universite)
admin.site.register(Faculte)
admin.site.register(Departement)
admin.site.register(Laboratoire)
