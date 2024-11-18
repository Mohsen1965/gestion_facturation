from django.urls import path
from .views import list_tva, create_tva, update_tva, delete_tva

urlpatterns = [
    path('', list_tva, name='list_tva'),
    path('create/', create_tva, name='create_tva'),
    path('update/<int:tva_id>/', update_tva, name='update_tva'),  # Removed 'views.'
    path('delete/<int:tva_id>/', delete_tva, name='delete_tva'),
]
