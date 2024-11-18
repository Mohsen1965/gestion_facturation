from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_clients, name='list_clients'),
    path('create/', views.create_client, name='create_client'),
    path('update/<int:pk>/', views.update_client, name='update_client'),
    path('afficher/<int:pk>/', views.afficher_client, name='afficher_client'),

    path('delete/<int:pk>/', views.delete_client, name='delete_client'), 
     # Assurez-vous que cette ligne est correcte

]
