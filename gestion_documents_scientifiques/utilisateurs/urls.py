from django.urls import path

from .views import register, registerProfesseur, registerThesard, confirmEmail

urlpatterns = [
    path('register/', register, name="register"),
    path('register/thesard/', registerThesard, name="register-thesard"),
    path('register/professeur/', registerProfesseur, name="register-professeur"),
    path('confirm-email/<uidb64>/<token>/', confirmEmail, name="confirm-email"),
]