from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('clients/', include('client.urls')),  # Correct path for the clients application
    path('articles/', include('article.urls')),  # Includes URLs from the articles application
    path('categorie_article/', include('categorie_article.urls')),  # Includes URLs from the category application
    path('factures/', include('facture.urls')),  # Correctly includes URLs from the facture application
    path('tva/', include('tva.urls')),  # Correctly includes URLs from the facture application
    path('devis/', include('devis.urls')),  # Correctly includes URLs from the facture application


    # Add other paths here if necessary
]
