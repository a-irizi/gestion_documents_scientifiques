import uuid
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage

from .models import Chercheur, Professeur, Thesard

from .forms import ChercheurForm, ProfesseurForm, ThesardForm
from .tokens import tokenGenerator

# Create your views here.
def register(request):
    return render(request, 'utilisateurs/register.html')

def sendEmailConfirmationEmail(user, toEmail):
    mail_subject = 'Valider votre e-mail'
    message = render_to_string('utilisateurs/email-confirmation-email.html', {
        'user': user,
        'domain': '127.0.0.1:8000',
        'uid': urlsafe_base64_encode(force_bytes(user.chercheur.utilisateur.pk)),
        'token': tokenGenerator.make_token(user),
    })
    email = EmailMessage(
                mail_subject, message, to=[toEmail]
    )
    email.content_subtype = "html"
    email.send()

def sendThesardAccountConfirmationEmail(user, toEmail):
    mail_subject = 'Valider Un compte thesard'
    message = render_to_string('utilisateurs/thesard-account-confirmation-email.html', {
        'user': user,
        'domain': '127.0.0.1:8000',
        'uid1': urlsafe_base64_encode(force_bytes(user.chercheur.thesard.directeurThese.chercheur.utilisateur.pk)),
        'uid2': urlsafe_base64_encode(force_bytes(user.chercheur.utilisateur.pk)),
        'token': tokenGenerator.make_token(user.chercheur.thesard.directeurThese.chercheur.utilisateur),
    })
    email = EmailMessage(
                mail_subject, message, to=[toEmail]
    )
    email.content_subtype = "html"
    email.send()


def registerThesard(request:HttpRequest):
    if request.method == "POST":
        thesardForm = ThesardForm(request.POST)
        if thesardForm.is_valid():
            utilisateur, chercheur, thesard = thesardForm.save(commit=False)
            utilisateur.save()
            chercheur.save()
            thesard.save()
            sendEmailConfirmationEmail(utilisateur, utilisateur.email)
            return render(request, 'utilisateurs/page-instruction-validation-email.html')
    thesardForm = ThesardForm()
    context = {'thesardForm': thesardForm,}

    return render(request, 'utilisateurs/register-thesard.html', context=context)

def registerProfesseur(request):
    if request.method == "POST":
        professeurForm = ProfesseurForm(request.POST)
        if professeurForm.is_valid():
            utilisateur, chercheur, professeur = professeurForm.save(commit=False)
            utilisateur.save()
            chercheur.save()
            professeur.save()
            sendEmailConfirmationEmail(utilisateur, utilisateur.email)
            return render(request, 'utilisateurs/page-instruction-validation-email.html')
    chercheurForm = ChercheurForm()
    context = {
        # 'utilisateurForm': utilisateurForm,
        'chercheurForm': chercheurForm,
    }

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
    if chercheur is not None and tokenGenerator.check_token(chercheur.utilisateur, token=token):
        chercheur.emailValide = True
        chercheur.save()
        if chercheur.type == Chercheur.ChercheurType.THESARD:
            # send notification to directeur de thése
            utilisateur =  chercheur.utilisateur
            toEmail = chercheur.thesard.directeurThese.chercheur.utilisateur.email
            sendThesardAccountConfirmationEmail(utilisateur, toEmail)
            return render(request, 'utilisateurs/page-instruction-apres-validation-email-thesard.html')
        elif chercheur.type == Chercheur.ChercheurType.PROFESSEUR:
            # send notification to directeur de departement
            return HttpResponse("you are a professeur")
    else:
        return HttpResponse(f"uid : {uid}, user uid: {chercheur.utilisateur.pk}, checktoken = {tokenGenerator.check_token(chercheur.utilisateur, token=token)}")

def notifyAccountValidation(toEmail):
    mail_subject = 'Valider Un compte thesard'
    message = render_to_string('utilisateurs/message-validation-compte.html', {
        'domain': '127.0.0.1:8000',
    })
    email = EmailMessage(
                mail_subject, message, to=[toEmail]
    )
    email.content_subtype = "html"
    email.send()


def confirmThesardAccount(request, prof_uidb64, thesard_uidb64, token):
    professeur = None
    puid = None
    thesard = None
    tuid = None
    try:
        puid = uuid.UUID((force_str(urlsafe_base64_decode(prof_uidb64))))
        professeur = Professeur.objects.get(chercheur__utilisateur__pk=puid)
    except(TypeError, ValueError, OverflowError, Professeur.DoesNotExist, Thesard.DoesNotExist):
        professeur = None
        uid = None

    try:
        tuid = uuid.UUID((force_str(urlsafe_base64_decode(thesard_uidb64))))
        thesard = Thesard.objects.get(chercheur__utilisateur__pk=tuid)
    except(TypeError, ValueError, OverflowError, Professeur.DoesNotExist, Thesard.DoesNotExist):
        professeur = None
        uid = None

    if professeur is not None and thesard is not None and tokenGenerator.check_token(professeur.chercheur.utilisateur, token=token):
        thesard.chercheur.utilisateur.is_active = True
        thesard.chercheur.utilisateur.save()
        notifyAccountValidation(thesard.chercheur.utilisateur.email)
        return render(request, 'utilisateurs/page-validation-compte.html')
    else:
        return HttpResponse(f"uid : {uid}, thesard: {thesard is not None}, professeur: {professeur is not None} checktoken = {tokenGenerator.check_token(professeur.chercheur.utilisateur, token=token)}")
