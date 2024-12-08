from django.shortcuts import render, get_object_or_404, redirect
from .models import Client
from .forms import ClientForm

def list_clients(request):
    # Par défaut, trier par 'created_at' en ordre décroissant
    clients = Client.objects.all().order_by('-created_at')

    context = {
        'clients': clients,
        'module_actif': 'Gestion des Clients'
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








from django.http import JsonResponse


def delete_clients(request):
    if request.method == 'POST':
        selected_clients = request.POST.get('selected_clients')  # Récupère les IDs envoyés
        print("Clients reçus :", selected_clients)  # Log pour vérifier

        if selected_clients:
            client_ids = selected_clients.split(',')  # Sépare les IDs
            try:
                # Supprime les clients correspondants
                Client.objects.filter(id__in=client_ids).delete()
                return JsonResponse({'status': 'success', 'message': 'Clients supprimés avec succès.'})
            except Exception as e:
                print("Erreur lors de la suppression :", e)  # Log en cas d'erreur
                return JsonResponse({'status': 'error', 'message': 'Erreur lors de la suppression.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Aucun client sélectionné.'})
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée.'})

def client_list_rechMultc(request):
    clients = Client.objects.all()

    # Vérifier si la recherche multicritère est demandée
    show_search = request.GET.get('show_search', False)
    
    # Ajouter une logique pour filtrer les clients si nécessaire
    field = request.GET.get('field', '')
    operator = request.GET.get('operator', '')
    value = request.GET.get('value', '')
    range_min = request.GET.get('range_min', None)
    range_max = request.GET.get('range_max', None)

    if field and operator and value:
        if operator == 'exact':
            clients = clients.filter(**{f'{field}__exact': value})
        elif operator == 'icontains':
            clients = clients.filter(**{f'{field}__icontains': value})
        elif operator == 'gt':
            clients = clients.filter(**{f'{field}__gt': value})
        elif operator == 'lt':
            clients = clients.filter(**{f'{field}__lt': value})
        elif operator == 'neq':
            clients = clients.exclude(**{f'{field}__exact': value})
        elif operator == 'lte':
            clients = clients.filter(**{f'{field}__lte': value})
        elif operator == 'gte':
            clients = clients.filter(**{f'{field}__gte': value})
        elif operator == 'range' and range_min and range_max:
            clients = clients.filter(**{f'{field}__range': (range_min, range_max)})

    return render(request, 'client/list_clients.html', {'clients': clients, 'show_search': show_search})
