from django.urls import path
from . import views


urlpatterns = [
    path('', views.list_articles, name='list_articles'),
    path('create/', views.create_article, name='create_article'),
    path('update/<int:pk>/', views.update_article, name='update_article'),
    path('delete/<int:pk>/', views.delete_article, name='delete_article'), 
    path('afficher/<int:pk>/', views.afficher_article, name='afficher_article'),

]
