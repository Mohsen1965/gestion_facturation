from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_categories, name='list_categories'),  # Liste des catégories
    path('create/', views.create_categorie, name='create_categorie'),
    path('update/<int:pk>/', views.update_categorie, name='update_categorie'),
    path('delete/<int:pk>/', views.delete_categorie, name='delete_categorie'),  # Suppression d'une catégorie
    path('delete_categories/', views.delete_categories, name='delete_categories'),
    path('afficher/<int:pk>/', views.afficher_categorie, name='afficher_categorie'),
    path('categories/delete/', views.delete_categories, name='delete_categories'),
    path('search/', views.categorie_list_rechMultc, name='categorie_list_rechMultc'),



]



