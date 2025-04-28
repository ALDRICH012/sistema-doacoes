from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Sum, Q
from django.utils import timezone
from django.utils.translation import gettext as _
from .models import Donor, Donation
from .forms import DonorForm, DonationForm

def donor_list(request):
    # Filtros
    search_query = request.GET.get('search', '')
    if search_query:
        donors = Donor.objects.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone__icontains=search_query)
        )
        if donors.exists():
            messages.info(request, f'Encontrados {donors.count()} doadores para "{search_query}"')
        else:
            messages.warning(request, f'Nenhum doador encontrado para "{search_query}"')
    else:
        donors = Donor.objects.all()

    # Paginação
    paginator = Paginator(donors, 10)  # 10 doadores por página
    page = request.GET.get('page')
    donors = paginator.get_page(page)
    
    # Estatísticas
    total_donations = Donation.objects.filter(status='completed').aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    today_donations = Donation.objects.filter(
        status='completed',
        date=timezone.now().date()
    ).count()
    
    context = {
        'donors': donors,
        'total_donations': total_donations,
        'today_donations': today_donations,
        'search_query': search_query
    }
    
    return render(request, 'doacoes/donor_list.html', context)

def add_donor(request):
    if request.method == 'POST':
        form = DonorForm(request.POST)
        if form.is_valid():
            donor = form.save()
            messages.success(request, 
                f'Doador {donor.name} cadastrado com sucesso! '
                f'Você pode agora registrar uma doação para este doador.'
            )
            return redirect('doacoes:donor_list')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = DonorForm()
    
    return render(request, 'doacoes/add_donor.html', {'form': form})

def add_donation(request):
    # Pré-seleciona o doador se fornecido na URL
    initial = {}
    donor_id = request.GET.get('donor')
    if donor_id:
        try:
            donor = get_object_or_404(Donor, id=donor_id)
            initial['donor'] = donor
            messages.info(request, f'Registrando doação para {donor.name}')
        except Donor.DoesNotExist:
            messages.warning(request, 'Doador não encontrado.')

    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save()
            messages.success(request, 
                f'Doação de R$ {donation.amount:.2f} registrada com sucesso para {donation.donor.name}! '
                f'Status: {donation.get_status_display()}'
            )
            return redirect('doacoes:donor_list')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = DonationForm(initial=initial)
    
    return render(request, 'doacoes/add_donation.html', {'form': form})

def handler404(request, exception):
    return render(request, '404.html', status=404)