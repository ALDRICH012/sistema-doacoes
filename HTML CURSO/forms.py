from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import Donor, Donation
import re

class DonorForm(forms.ModelForm):
    class Meta:
        model = Donor
        fields = ['name', 'email', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome completo'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'exemplo@email.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+5511999999999'
            })
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.startswith('+'):
            raise forms.ValidationError('O número deve começar com "+" (ex: +5511999999999)')
        
        # Remove tudo exceto dígitos e o "+"
        cleaned_phone = '+' + re.sub(r'[^\d]', '', phone[1:])
        
        if len(cleaned_phone) < 10:
            raise forms.ValidationError('Número muito curto (mínimo 10 dígitos)')
            
        return cleaned_phone

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError('Formato de e-mail inválido')
        
        if Donor.objects.filter(email=email).exists():
            raise forms.ValidationError('E-mail já cadastrado')
        return email

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['donor', 'amount', 'description', 'status']
        widgets = {
            'donor': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0.01'  # Valor mínimo de 1 centavo
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'status': forms.Select(attrs={'class': 'form-select'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['donor'].queryset = Donor.objects.all().order_by('name')
        
        # Labels customizados
        self.fields['amount'].label = 'Valor (R$)'
        self.fields['donor'].label = 'Doador'
        self.fields['description'].label = 'Descrição'
        self.fields['status'].label = 'Status'

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError('O valor deve ser positivo')
        return amount
