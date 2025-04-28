from django.db import models
from django.core.validators import RegexValidator

class Donor(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nome')
    email = models.EmailField(verbose_name='E-mail')
    phone = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message='O número de telefone deve estar no formato: +999999999'
            )
        ],
        verbose_name='Telefone'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data de criação')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última atualização')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Doador'
        verbose_name_plural = 'Doadores'
        ordering = ['-created_at']

class Donation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('completed', 'Concluída'),
        ('cancelled', 'Cancelada')
    ]

    donor = models.ForeignKey(Donor, on_delete=models.CASCADE, verbose_name='Doador')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor')
    date = models.DateField(auto_now_add=True, verbose_name='Data')
    description = models.TextField(blank=True, verbose_name='Descrição')
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Status'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data de criação')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última atualização')

    def __str__(self):
        return f'Doação de {self.amount} por {self.donor.name}'

    class Meta:
        verbose_name = 'Doação'
        verbose_name_plural = 'Doações'
        ordering = ['-date']