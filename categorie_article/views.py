from django.shortcuts import render, redirect, get_object_or_404
from .models import CategorieArticle
from .forms import CategorieArticleForm


def list_categories(request):
    categories = CategorieArticle.objects.all().order_by('-id')  # Trier par ordre décroissant de l'ID
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
    return render(request, 'form_categorie.html', {'form': form})

def update_categorie(request, pk):
    categorie = get_object_or_404(CategorieArticle, pk=pk)
    if request.method == 'POST':
        form = CategorieArticleForm(request.POST, instance=categorie)
        if form.is_valid():
            form.save()
            return redirect('list_categories')
    else:
        form = CategorieArticleForm(instance=categorie)
    return render(request, 'form_categorie.html', {'form': form})


def delete_categorie(request, pk):
    categorie = get_object_or_404(CategorieArticle, pk=pk)
    if request.method == 'POST':
        categorie.delete()
        return redirect('list_categories')
    return render(request, 'categorie_article/delete_categorie.html', {'categorie': categorie})
