from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include  # Add 'include' here
from .views import get_prix_unitaire
from .views import get_taux_tva



urlpatterns = [
    path('', views.list_factures, name='list_factures'),  # Path for listing invoices
    path('delete/<int:facture_id>/', views.delete_facture, name='delete_facture'),
    path('facture/<int:facture_id>/', views.afficher_facture, name='afficher_facture'),
    path('modifier/<int:facture_id>/', views.modifier_facture, name='modifier_facture'),
    path('facture/<int:facture_id>/pdf/', views.generate_facture_pdf, name='generate_facture_pdf'),

    path('create/', views.create_facture, name='create_facture'),  # Path for creating an invoice
    path('get-prix-unitaire/<int:article_id>/', views.get_prix_unitaire, name='get_prix_unitaire'),
    path('get-taux_tva/<int:article_id>/', views.get_taux_tva, name='get_taux_tva'),
    path('facture/delete/', views.delete_factures, name='delete_factures'),
    path('print/', views.print_factures, name='print_factures'),  # For printing selected invoices
    path('search/', views.list_facture_rechMultc, name='list_facture_rechMultc'),

    

    # Add other paths as necessary
]
