from types import CellType
from django import forms
from . import models
from django.contrib.auth.forms import ReadOnlyPasswordHashField
import etablissements

class UtilisateurCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = models.Utilisateur
        fields = ['prenom', 'deuxiemeNom', 'nom', 'email']
    
    field_order = ['prenom', 'deuxiemeNom', 'nom', 'email', 'password1', 'password2']
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UtilisateurChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()
    class Meta:
        model = models.Utilisateur
        fields = ('email', 'prenom', 'deuxiemeNom', 'nom',)

class chercheurCreationForm(forms.ModelChoiceField):
    class Meta:
        model = models.Chercheur
        fields = ['laboratoire']

class ThesardCreationForm(forms.ModelForm):
    class Meta:
        model = models.Thesard
        exclude = ['utilisateur', 'papier']
    
    def save(self, commit=True):
        user= super().save(commit=False)
        user.type = models.Chercheur.ChercheurType.THESARD
        if commit:
            user.save()
        return user

class ProfesseurCreationForm(forms.ModelForm):
    class Meta:
        model = models.Professeur
        exclude = ['isDirecteurLabo', 'utilisateur', 'papier']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.type = models.Chercheur.ChercheurType.PROFESSEUR
        user.isDirecteurLabo = False
        if commit:
            user.save()
        return user
