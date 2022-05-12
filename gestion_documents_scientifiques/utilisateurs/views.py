from django.http import HttpRequest
from django.shortcuts import render
from .forms import UtilisateurCreationForm, ThesardCreationForm

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
            return render(request, 'utilisateurs/page-instruction-validation-email.html')
    utilisateurForm = UtilisateurCreationForm()
    thesardForm = ThesardCreationForm()
    context = {'chercheurForm': utilisateurForm,'thesardForm': thesardForm,}

    return render(request, 'utilisateurs/register-thesard.html', context=context)

def registerProfesseur(request):
    return render(request, 'utilisateurs/register-professeur.html')
