from django.urls import path

from .views import register, registerProfesseur, registerThesard

urlpatterns = [
    path('register/', register, name="register"),
    path('register/thesard/', registerThesard, name="register-thesard"),
    path('register/professeur/', registerProfesseur, name="register-professeur"),
]