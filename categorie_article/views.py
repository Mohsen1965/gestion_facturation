from django.shortcuts import render, redirect, get_object_or_404
from .models import CategorieArticle
from .forms import CategorieArticleForm
from django.http import JsonResponse
from django.contrib import messages
from .forms import CategorieArticleSearchForm





def list_categories(request):
    categories = CategorieArticle.objects.all().order_by('-created_at')  # Trier par ordre décroissant de l'ID
    context = {
        'categories': categories,
        'module_actif': 'Gestion des Categories Article'  # Module actif à passer au template
    }
    return render(request, 'categorie_article/list_categories.html', context)

def create_categorie(request):
    if request.method == 'POST':
        form = CategorieArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_categories')
    else:
        form = CategorieArticleForm()

    return render(request, 'categorie_article/create_categorie.html', {'form': form})


def update_categorie(request, pk):
    categorie = get_object_or_404(CategorieArticle, pk=pk)
    if request.method == 'POST':
        form = CategorieArticleForm(request.POST, instance=categorie)
        if form.is_valid():
            form.save()
            return redirect('list_categories')
    else:
        form = CategorieArticleForm(instance=categorie)
    return render(request, 'categorie_article/update_categorie.html', {'form': form})


def delete_categorie(request, pk):
    categorie = get_object_or_404(CategorieArticle, pk=pk)
    if request.method == 'POST':
        categorie.delete()
        return redirect('list_categories')
    return render(request, 'categorie_article/delete_categorie.html', {'categorie': categorie})



def afficher_categorie(request, pk):
    # Récupérer une seule catégorie avec l'ID (pk)
    categorie = get_object_or_404(CategorieArticle, pk=pk)
    
    # Rendre la page avec la catégorie récupérée
    return render(request, 'afficher_categorie.html', {'categorie': categorie})





def delete_categories(request):
    if request.method == 'POST':
        selected_categories = request.POST.get('selected_categories', '')
        print(f"Selected categories: {selected_categories}")  # Affiche les IDs reçus

        if selected_categories:
            ids = selected_categories.split(',')
            print(f"IDs to delete: {ids}")  # Vérifie les IDs séparés

            try:
                # Tente de supprimer les catégories
                CategorieArticle.objects.filter(id__in=ids).delete()
                return JsonResponse({'status': 'success', 'message': 'Les catégories sélectionnées ont été supprimées.'})
            except Exception as e:
                print(f"Error deleting categories: {e}")  # Affiche l'erreur en cas de problème
                return JsonResponse({'status': 'error', 'message': f'Une erreur est survenue lors de la suppression: {str(e)}'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Aucune catégorie sélectionnée.'})


def categorie_list_rechMultc(request):
    categories = CategorieArticle.objects.all()
    
    # Vérifier si la recherche multicritère est demandée
    show_search = request.GET.get('show_search', False)
    
    # Initialiser le formulaire de recherche
    form = CategorieArticleSearchForm(request.GET)
    
    # Ajouter une logique pour filtrer les catégories si nécessaire
    field = request.GET.get('field', '')
    operator = request.GET.get('operator', '')
    value = request.GET.get('value', '')
    range_min = request.GET.get('range_min', None)
    range_max = request.GET.get('range_max', None)

    if form.is_valid():
        if field and operator and value:
            if operator == 'exact':
                categories = categories.filter(**{f'{field}__exact': value})
            elif operator == 'icontains':
                categories = categories.filter(**{f'{field}__icontains': value})
            elif operator == 'gt':
                categories = categories.filter(**{f'{field}__gt': value})
            elif operator == 'lt':
                categories = categories.filter(**{f'{field}__lt': value})
            elif operator == 'lte':
                categories = categories.filter(**{f'{field}__lte': value})
            elif operator == 'gte':
                categories = categories.filter(**{f'{field}__gte': value})
            elif operator == 'range' and range_min and range_max:
                categories = categories.filter(**{f'{field}__range': (range_min, range_max)})

    return render(request, 'categorie_article/list_categories.html', {
        'categories': categories,
        'show_search': show_search,
        'form': form
    })
