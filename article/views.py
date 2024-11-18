from django.shortcuts import render, get_object_or_404, redirect
from .models import Article
from .models import TVA
from .models import CategorieArticle
from .forms import ArticleForm




def list_articles(request):
    # Par défaut, le tri est ascendant
    sort = request.GET.get('sort', 'nom')  # Trier par nom par défaut si aucun paramètre de tri n'est fourni
    direction = request.GET.get('direction', 'asc')  # Par défaut, le tri est ascendant

    # Déterminer le champ de tri en fonction du paramètre et de la direction
    if direction == 'desc':
        sort = f'-{sort}'  # Préfixer par '-' pour un tri décroissant

    articles = Article.objects.all().order_by(sort)

    context = {
        'articles': articles,
        'current_sort': request.GET.get('sort', 'nom'),
        'current_direction': direction,
        'module_actif': 'Gestion des Articles'  # Module actif à passer au template

    }

    return render(request, 'article/list_articles.html', context)


def create_article(request):
    print("create_article view called")

    # Charger les catégories et les TVA triées par nom ou taux
    categories = CategorieArticle.objects.all().order_by('nom')  # Assurez-vous que 'nom' est le bon champ
    tvas = TVA.objects.all().order_by('taux_tva')  # Assurez-vous que 'taux_tva' est le bon champ

    # Débogage pour afficher les catégories et TVA triées
    print(f"Categories triées : {[categorie.nom for categorie in categories]}")
    print(f"TVAs triées : {[str(tva.taux_tva) for tva in tvas]}")

    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_articles')
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