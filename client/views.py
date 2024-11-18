from django.shortcuts import render, get_object_or_404, redirect
from .models import Client
from .forms import ClientForm

def list_clients(request):
    clients = Client.objects.all().order_by('-id')  # Trier par ordre décroissant de l'ID
    context = {
        'clients': clients,
        'module_actif': 'Gestion des Clients'  # Module actif à passer au template
    }
    return render(request, 'client/list_clients.html', context)

def create_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_clients')  # Rediriger vers la liste des clients après la création
    else:
        form = ClientForm()
    
    return render(request, 'client/create_client.html', {'form': form})

def update_client(request, pk):
    client = get_object_or_404(Client, pk=pk)  # Ensure client is fetched
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('list_clients')
    else:
        form = ClientForm(instance=client)
    return render(request, 'client/update_client.html', {'form': form, 'client': client})  # Pass 'client' to template

def delete_client(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        client.delete()
        return redirect('list_clients')
    return render(request, 'client/delete_client.html', {'client': client})



def afficher_client(request, pk):
    # Fetch the client using the primary key
    client = get_object_or_404(Client, pk=pk)
    
    # Render the client details template and pass the client object to the template
    return render(request, 'client/afficher_client.html', {'client': client})