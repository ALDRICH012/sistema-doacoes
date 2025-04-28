from django.urls import path
from .views import donor_list, add_donor, add_donation

app_name = 'doacoes'

urlpatterns = [
    path('', donor_list, name='donor_list'),
    path('doador/novo/', add_donor, name='add_donor'),
    path('doacao/nova/', add_donation, name='add_donation'),
]
