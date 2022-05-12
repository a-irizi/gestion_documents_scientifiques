import uuid
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage

from utilisateurs.models import Chercheur, Professeur, Thesard

from .forms import ProfesseurCreationForm, UtilisateurCreationForm, ThesardCreationForm
from .tokens import emailActivationToken

# Create your views here.
def register(request):
    return render(request, 'utilisateurs/register.html')

def sendEmailConfirmationEmail(user, toEmail):
    mail_subject = 'Valider votre e-mail'
    message = render_to_string('utilisateurs/email-confirmation-email.html', {
        'user': user,
        'domain': '127.0.0.1:8000',
        'uid': urlsafe_base64_encode(force_bytes(user.utilisateur.pk)),
        'token':emailActivationToken.make_token(user),
    })
    print(message)
    email = EmailMessage(
                mail_subject, message, to=[toEmail]
    )
    email.content_subtype = "html"
    email.send()

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
            thesard.emailValide = False
            thesard.save()
            sendEmailConfirmationEmail(thesard, utilisateur.email)
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
            sendEmailConfirmationEmail(professeur, utilisateur.email)
            return render(request, 'utilisateurs/page-instruction-validation-email.html')
    utilisateurForm = UtilisateurCreationForm()
    professeurForm = ProfesseurCreationForm()
    context = {'chercheurForm': utilisateurForm, 'professeurForm': professeurForm}

    return render(request, 'utilisateurs/register-professeur.html', context=context)


def confirmEmail(request, uidb64, token):
    chercheur : Chercheur = None
    uid = None
    try:
        uid = uuid.UUID((force_str(urlsafe_base64_decode(uidb64))))
        chercheur = Chercheur.objects.get(utilisateur__pk=uid)
    except(TypeError, ValueError, OverflowError, Chercheur.DoesNotExist):
        chercheur = None
        uid = None
    if chercheur is not None and emailActivationToken.check_token(chercheur, token=token):
        if chercheur.type == Chercheur.ChercheurType.THESARD:
            thesard = Thesard.objects.get(pk=uid)
            thesard.emailValide = True
            thesard.save()
            # send notification to directeur de thése
            # thesard = Thesard.objects.get(pk=uid)
            
            return HttpResponse("you are a thesard")
        elif chercheur.type == Chercheur.ChercheurType.PROFESSEUR:
            professeur = Professeur.objects.get(pk=uid)
            professeur.emailValide = True
            professeur.save()

            return HttpResponse("you are a professeur")
    else:
        return HttpResponse(f"uid : {uid}, user uid: {chercheur.utilisateur.pk}, checktoken = {emailActivationToken.check_token(chercheur, token=token)}")
