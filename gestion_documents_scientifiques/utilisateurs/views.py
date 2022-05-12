import uuid
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage

from utilisateurs.models import Chercheur

from .forms import ChercheurForm, ProfesseurForm, ThesardForm
from .tokens import emailActivationToken

# Create your views here.
def register(request):
    return render(request, 'utilisateurs/register.html')

def sendEmailConfirmationEmail(user, toEmail):
    mail_subject = 'Valider votre e-mail'
    message = render_to_string('utilisateurs/email-confirmation-email.html', {
        'user': user,
        'domain': '127.0.0.1:8000',
        'uid': urlsafe_base64_encode(force_bytes(user.chercheur.utilisateur.pk)),
        'token': emailActivationToken.make_token(user),
    })
    print(message)
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
    if chercheur is not None and emailActivationToken.check_token(chercheur.utilisateur, token=token):
        chercheur.emailValide = True
        chercheur.save()
        if chercheur.type == Chercheur.ChercheurType.THESARD:
            # send notification to directeur de thése            
            return HttpResponse("you are a thesard")
        elif chercheur.type == Chercheur.ChercheurType.PROFESSEUR:
            # send notification to directeur de departement
            return HttpResponse("you are a professeur")
    else:
        return HttpResponse(f"uid : {uid}, user uid: {chercheur.utilisateur.pk}, checktoken = {emailActivationToken.check_token(chercheur, token=token)}")
