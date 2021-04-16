"""Definiuje wzorce adresów URL dla aplikacji users."""
from django.urls import path, include
from . import views
from django.conf.urls import url
app_name = 'users'
urlpatterns = [
    # Dołączenie domyślnych adresów URL uwierzytelniania.
    path('', include('django.contrib.auth.urls')),
    # Strona rejestracji.
    url('register/', views.register, name='register'),
]