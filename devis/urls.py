from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include  # Add 'include' here
from .views import get_prix_unitaire
from .views import get_taux_tva
from .views import transferer_devis_en_facture



urlpatterns = [
    path('', views.list_devis, name='list_devis'),  # Path for listing invoices
    path('delete/<int:devis_id>/', views.delete_devis, name='delete_devis'),
    path('devis/<int:devis_id>/', views.afficher_devis, name='afficher_devis'),
    path('modifier/<int:devis_id>/', views.modifier_devis, name='modifier_devis'),
    path('devis/<int:devis_id>/pdf/', views.generate_devis_pdf, name='generate_devis_pdf'),

    path('create/', views.create_devis, name='create_devis'),  # Path for creating an invoice
    path('get-prix-unitaire/<int:article_id>/', views.get_prix_unitaire, name='get_prix_unitaire'),
    path('get-taux_tva/<int:article_id>/', views.get_taux_tva, name='get_taux_tva'),
    path('devis/<int:devis_id>/transferer_en_facture/', transferer_devis_en_facture, name='transferer_devis_en_facture'),
    path('devis/delete/', views.delete_deviss, name='delete_deviss'),

    # Add other paths as necessary
]
