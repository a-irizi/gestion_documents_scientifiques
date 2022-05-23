import email
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

class ChercheurForm(forms.Form):
    prenom = forms.CharField(label="Prenom", max_length=200, required=True)
    nom= forms.CharField(label="Nom", max_length=200, required=True)
    deuxiemeNom = forms.CharField(label="Deuxieme Nom", max_length=200, required=False)
    email = forms.EmailField(label="Email", max_length=200, required=True)
    password1 = forms.CharField(label="Mot de passe", max_length=200, required=True, widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmer mot de passe", max_length=200, required=True, widget=forms.PasswordInput)

    labos = models.Laboratoire.objects.all()
    laboratoire = forms.ModelChoiceField(label="Laboratoire", queryset=labos, required=True, widget=forms.Select)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Les mots de passe ne correspondent pas")
        return password2
    
    def save(self, commit=True):
        prenom = self.cleaned_data["prenom"]
        nom= self.cleaned_data["nom"]
        deuxiemeNom = self.cleaned_data["deuxiemeNom"]
        email = self.cleaned_data["email"]
        password = self.cleaned_data["password2"]

        laboratoire =  self.cleaned_data["laboratoire"]

        utilisateur = models.Utilisateur(nom=nom, prenom=prenom, deuxiemeNom=deuxiemeNom, email=email)
        utilisateur.set_password(password)
        utilisateur.is_active = False;
        
        chercheur = models.Chercheur(utilisateur=utilisateur, laboratoire=laboratoire)
        chercheur.emailValide = False

        if commit:
            utilisateur.save()
            chercheur.save()
        return (utilisateur, chercheur)

class ProfesseurForm(ChercheurForm):

    def save(self, commit=True):
        utilisateur, chercheur = super().save(commit=False)
        chercheur.type = models.Chercheur.ChercheurType.PROFESSEUR
        professeur = models.Professeur()
        professeur.chercheur = chercheur
        professeur.isDirecteurLabo = False
        if commit:
            utilisateur.save()
            chercheur.save()
            professeur.save()
        return utilisateur, chercheur, professeur

class ThesardForm(ChercheurForm):
    anneeDebutDoctorat = forms.IntegerField(label="Annee du début de doctorat", required=True)
    sujetThese = forms.CharField(label="Sujet du thése", max_length=200, required=True)

    directeursT = models.Professeur.objects.filter(chercheur__utilisateur__is_active=True)
    directeurThese = forms.ModelChoiceField(label="Directeur de These", queryset=directeursT, required=True, widget=forms.Select)

    def save(self, commit=True):
        anneeDebutDoctorat = self.cleaned_data["anneeDebutDoctorat"]
        sujetThese = self.cleaned_data["sujetThese"]
        directeurThese = self.cleaned_data["directeurThese"]

        utilisateur, chercheur = super().save(commit=False)

        chercheur.type = models.Chercheur.ChercheurType.THESARD
        thesard = models.Thesard(anneeDebutDoctorat=anneeDebutDoctorat, sujetThese=sujetThese, directeurThese=directeurThese)
        thesard.chercheur = chercheur
        if commit:
            utilisateur.save()
            chercheur.save()
            thesard.save()
        return utilisateur, chercheur, thesard
