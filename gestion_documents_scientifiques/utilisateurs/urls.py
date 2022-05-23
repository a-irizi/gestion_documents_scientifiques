from django.urls import path

from .views import confirmProfesseurAccount, confirmThesardAccount, loginUser, logoutUser, register, registerProfesseur, registerThesard, confirmEmail

urlpatterns = [
    path('register/', register, name="register"),
    path('register/thesard/', registerThesard, name="register-thesard"),
    path('register/professeur/', registerProfesseur, name="register-professeur"),
    path('confirm-email/<uidb64>/<token>/', confirmEmail, name="confirm-email"),
    path('confirm-thesard-account/<prof_uidb64>/<thesard_uidb64>/<token>/', confirmThesardAccount, name="confirm-thesard-account"),
    path('confirm-professeur-account/<directeurLabo_uidb64>/<prof_uidb64>/<token>/', confirmProfesseurAccount,name="confirm-professeur-account"),

    path('login/', loginUser, name='login'),
    path('logout/', logoutUser, name='logout'),
]
    