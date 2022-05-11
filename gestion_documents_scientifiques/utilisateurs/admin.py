from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Utilisateur, Thesard
from .forms import UtilisateurCreationForm, UtilisateurChangeForm
# Register your models here.


class UtilisateurAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UtilisateurChangeForm
    add_form = UtilisateurCreationForm
    model = Utilisateur

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'nom', 'prenom', 'is_superuser')
    list_filter = ('is_superuser',)
    fieldsets = (
        ('Identification', {'fields': ('email', 'password')}),
        ('Information Personelles', {
         'fields': ('nom', 'deuxiemeNom', 'prenom',)}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff', 'is_active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        ('Identification', {'fields': ('email', 'password1', 'password2')}),
        ('Information Personelles', {
         'fields': ('nom', 'deuxiemeNom', 'prenom',)}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff', 'is_active')}),
    )
    search_fields = ('email', 'nom', 'prenom')
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(Utilisateur, UtilisateurAdmin)
admin.site.register(Thesard)
