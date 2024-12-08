from django.shortcuts import render, get_object_or_404, redirect
from .models import Article
from .forms import ArticleForm

from django.http import JsonResponse
from .models import CategorieArticle, TVA
from .forms import ArticleSearchForm




def list_articles(request):
    # Par défaut, le tri est ascendant
    sort = request.GET.get('sort', 'nom')  # Trier par nom par défaut si aucun paramètre de tri n'est fourni
    direction = request.GET.get('direction', 'asc')  # Par défaut, le tri est ascendant

    # Déterminer le champ de tri en fonction du paramètre et de la direction
    if direction == 'desc':
        sort = f'-{sort}'  # Préfixer par '-' pour un tri décroissant

    articles = Article.objects.all().order_by('-created_at')

    # Gestion de la recherche
    query = request.GET.get('q', '')  # Récupère la valeur du champ de recherche
    if query:
        articles = articles.filter(
            Q(code_article__icontains=query) |
            Q(nom__icontains=query) |
            Q(description__icontains=query) |
            Q(categorie__nom__icontains=query) |
            Q(tva__taux_tva__icontains=query)
        )

    articles = Article.objects.all().order_by('-created_at')

    context = {
        'articles': articles,
        'current_sort': request.GET.get('sort', 'nom'),
        'current_direction': direction,
        'module_actif': 'Gestion des Articles'  # Module actif à passer au template
    }

    return render(request, 'article/list_articles.html', context)


def create_article(request):
    print("create_article view called")

    articles = Article.objects.all()
    categories = CategorieArticle.objects.all()
    tvas = TVA.objects.all()

    # Check if categories and tvas have data
   
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            print("Form is valid, saving the article")
            form.save()
            print("Article saved successfully")
            return redirect('list_articles')
        else:
            print("Form is not valid")
            print(form.errors)  # Print form errors for debugging
    else:
        form = ArticleForm()

    return render(request, 'article/create_article.html', {
        'form': form,
        'categories': categories,
        'tvas': tvas
    })


def update_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('list_articles')
    else:
        form = ArticleForm(instance=article)
    return render(request, 'article/update_article.html', {'form': form})

def delete_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        article.delete()
        return redirect('list_articles')
    return render(request, 'article/delete_article.html', {'article': article})

def afficher_article(request, pk):
    # Fetch the client using the primary key
    article = get_object_or_404(Article, pk=pk)
    
    # Render the client details template and pass the client object to the template
    return render(request, 'article/afficher_article.html', {'article': article})


def update_article(request, pk):
    article = get_object_or_404(Article, pk=pk)  # Fetch the article by primary key
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('list_articles')  # Redirect to the list of articles
    else:
        form = ArticleForm(instance=article)
    return render(request, 'article/update_article.html', {'form': form, 'article': article})  # Pass 'article' to the template


def categories_autocomplete(request):
    if 'q' in request.GET:
        query = request.GET.get('q')
        categories = CategorieArticle.objects.filter(nom__icontains=query).values('id', 'nom')
        results = [{'id': cat['id'], 'text': cat['nom']} for cat in categories]
        return JsonResponse({'results': results})
    return JsonResponse({'results': []})

def tva_autocomplete(request):
    if 'q' in request.GET:
        query = request.GET.get('q')
        tva_items = TVA.objects.filter(taux_tva__icontains=query).values('id', 'taux_tva')
        results = [{'id': tva['id'], 'text': f"{tva['taux_tva']}%"} for tva in tva_items]
        return JsonResponse({'results': results})
    return JsonResponse({'results': []})

def delete_articles(request):
    if request.method == 'POST':
        selected_ids = request.POST.get('selected_articles', '')  # Récupérer les IDs des articles sélectionnés
        if selected_ids:
            selected_ids_list = [int(id) for id in selected_ids.split(',')]  # Conversion des IDs en liste
            print(f"Articles sélectionnés pour suppression (avant suppression) : {selected_ids_list}")  # Log des IDs reçus
            
            # Suppression des articles sélectionnés
            articles_deleted, deleted_objects = Article.objects.filter(id__in=selected_ids_list).delete()
            
            # Obtenir uniquement le nombre d'articles supprimés
            articles_count = deleted_objects.get('article.Article', 0)  # Remplacer 'app' par votre nom d'application
            
            if articles_count > 0:
                # Retourner le nombre d'articles supprimés dans la réponse
                return JsonResponse({'status': 'success', 'message': f'{articles_count} articles supprimés avec succès.'})
            else:
                return JsonResponse({'status': 'warning', 'message': "Aucun article trouvé à supprimer."})
        else:
            return JsonResponse({'status': 'warning', 'message': "Aucun article sélectionné."})
    
    return JsonResponse({'status': 'error', 'message': "Méthode non autorisée."})  




def article_list_rechMultc(request):
    articles = Article.objects.all()
    
    # Vérifier si la recherche multicritère est demandée
    show_search = request.GET.get('show_search', False)
    
    # Ajouter une logique pour filtrer les articles si nécessaire
    field = request.GET.get('field', '')
    operator = request.GET.get('operator', '')
    value = request.GET.get('value', '')
    range_min = request.GET.get('range_min', None)
    range_max = request.GET.get('range_max', None)

    if field and operator and value:
        if operator == 'exact':
            articles = articles.filter(**{f'{field}__exact': value})
        elif operator == 'icontains':
            articles = articles.filter(**{f'{field}__icontains': value})
        elif operator == 'gt':
            articles = articles.filter(**{f'{field}__gt': value})
        elif operator == 'lt':
            articles = articles.filter(**{f'{field}__lt': value})
        elif operator == 'neq':
            articles = articles.exclude(**{f'{field}__exact': value})
        elif operator == 'lte':
            articles = articles.filter(**{f'{field}__lte': value})
        elif operator == 'gte':
            articles = articles.filter(**{f'{field}__gte': value})
        elif operator == 'range' and range_min and range_max:
            articles = articles.filter(**{f'{field}__range': (range_min, range_max)})

    return render(request, 'article/list_articles.html', {'articles': articles, 'show_search': show_search})
