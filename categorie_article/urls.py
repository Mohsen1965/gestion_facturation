from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_categories, name='list_categories'),
    path('categories/create/', views.create_categorie, name='create_categorie'),
    path('categories/update/<int:pk>/', views.update_categorie, name='update_categorie'),
    path('delete/<int:pk>/', views.delete_categorie, name='delete_categorie'), 


]
