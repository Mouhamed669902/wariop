from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Django cherchera automatiquement dans templates/registration/login.html
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Ta route d'inscription des vendeurs
    path('inscription-vendeur/', views.inscription_vendeur, name='inscription_vendeur'),
]