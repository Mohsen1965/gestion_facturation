from django.urls import path
from . import views


urlpatterns = [
    path('', views.list_articles, name='list_articles'),
    path('create/', views.create_article, name='create_article'),
    path('update/<int:pk>/', views.update_article, name='update_article'),
    path('delete/<int:pk>/', views.delete_article, name='delete_article'), 
    path('afficher/<int:pk>/', views.afficher_article, name='afficher_article'),
    path('article/delete/', views.delete_articles, name='delete_articles'),

    path('categories-autocomplete/', views.categories_autocomplete, name='categories_autocomplete'),
    path('tva-autocomplete/', views.tva_autocomplete, name='tva_autocomplete'),
    path('search/', views.article_list_rechMultc, name='article_list_rechMultc'),

]
