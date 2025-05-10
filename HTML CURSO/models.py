from django.db import models
from django.core.validators import RegexValidator, MinValueValidator

class Donor(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nome')
    email = models.EmailField(unique=True, verbose_name='E-mail')  # Unique para evitar duplicatas
    phone = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\+\d{9,15}$',
                message='Use o formato: +5511999999999'
            )
        ],
        verbose_name='Telefone'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Doadores'
        ordering = ['-created_at']

class Donation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('completed', 'Concluída'),
        ('cancelled', 'Cancelada')
    ]

    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]  # Valor mínimo de 1 centavo
    )
    date = models.DateField(auto_now_add=True)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'R$ {self.amount} - {self.donor.name}'

    class Meta:
        verbose_name_plural = 'Doações'
        ordering = ['-date']
