from django.http import HttpRequest
from django.shortcuts import render

from utilisateurs.models import Professeur
from .forms import ProfesseurCreationForm, UtilisateurCreationForm, ThesardCreationForm

# Create your views here.
def register(request):
    return render(request, 'utilisateurs/register.html')

def registerThesard(request:HttpRequest):
    if request.method == "POST":
        utilisateurForm = UtilisateurCreationForm(request.POST)
        thesardForm = ThesardCreationForm(request.POST)
        if utilisateurForm.is_valid() and thesardForm.is_valid():
            utilisateur = utilisateurForm.save(commit=False)
            utilisateur.is_active = False
            utilisateur.save()
            thesard = thesardForm.save(commit=False)
            thesard.utilisateur = utilisateur
            thesard.save()
            return render(request, 'utilisateurs/page-instruction-validation-email.html')
    utilisateurForm = UtilisateurCreationForm()
    thesardForm = ThesardCreationForm()
    context = {'chercheurForm': utilisateurForm,'thesardForm': thesardForm,}

    return render(request, 'utilisateurs/register-thesard.html', context=context)

def registerProfesseur(request):
    if request.method == "POST":
        utilisateurForm = UtilisateurCreationForm(request.POST)
        professeurForm = ProfesseurCreationForm(request.POST)
        if utilisateurForm.is_valid() and professeurForm.is_valid():
            utilisateur = utilisateurForm.save(commit=False)
            utilisateur.is_active = False
            utilisateur.save()
            professeur = professeurForm.save(commit=False)
            professeur.utilisateur = utilisateur
            professeur.save()
            return render(request, 'utilisateurs/page-instruction-validation-email.html')
    utilisateurForm = UtilisateurCreationForm()
    professeurForm = ProfesseurCreationForm()
    context = {'chercheurForm': utilisateurForm, 'professeurForm': professeurForm}

    return render(request, 'utilisateurs/register-professeur.html', context=context)
