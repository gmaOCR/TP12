from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from authentication.models import User
from .models import Client, Contract, Event
from .forms import ClientForm, ContractForm

@login_required
def staff(request):
    users = User.objects.all()
    context = {
        'users': users,
    }

    return render(request, 'sales/staff.html', context)

@login_required
def clients(request):
    clients = Client.objects.select_related('sales_contact').all()
    context = {
        'clients': clients,
    }

    return render(request, 'sales/clients.html', context)

@login_required
def contracts(request):
    contracts = Contract.objects.select_related('sales_contact', 'client').all()

    context = {
        'contracts': contracts,
    }

    return render(request, 'sales/contracts.html', context)

@login_required
def events(request):
    events = Event.objects.select_related('support_contact','client__sales_contact').all()

    context = {
        'events': events,
    }

    return render(request, 'sales/events.html', context)

@login_required
def create_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Le client a été créé avec succès.')
            return redirect('clients')
    else:
        form = ClientForm()

    context = {'form': form}
    return render(request, 'sales/create_form.html', context)

@login_required
def edit_client(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if 'edit_client' in request.POST:
            form = ClientForm(request.POST, instance=client, files=request.FILES)
            if form.is_valid():
                form.save()
                return redirect('clients')
    else:
        form = ClientForm(instance=client)
    context = {'form': form}
    return render(request, 'sales/create_form.html', context)

@login_required
def delete_client(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == 'POST':
        client.delete()
        return redirect('clients')
    context = {'client': client}
    return render(request, 'sales/delete_client_confirm.html', context)

@login_required
def create_contract(request):
    if request.method == 'POST':
        form = ContractForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Le contrat a été créé avec succès.')
            return redirect('contracts')
    else:
        form = ContractForm()

    context = {'form': form}
    return render(request, 'sales/create_form.html', context)