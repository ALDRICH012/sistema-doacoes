from django import forms
from .models import Donor, Donation

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
                'placeholder': '+999999999'
            })
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.startswith('+'):
            raise forms.ValidationError('O número de telefone deve começar com +')
        return phone

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['donor', 'amount', 'description', 'status']
        widgets = {
            'donor': forms.Select(attrs={
                'class': 'form-select'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descrição da doação',
                'rows': 3
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ordena os doadores por nome
        self.fields['donor'].queryset = Donor.objects.all().order_by('name')
        
        # Adiciona classes Bootstrap aos labels
        for field_name, field in self.fields.items():
            field.label_suffix = ''
            if field_name == 'amount':
                field.label = 'Valor (R$)'
            elif field_name == 'donor':
                field.label = 'Doador'
            elif field_name == 'description':
                field.label = 'Descrição'
            elif field_name == 'status':
                field.label = 'Status' 