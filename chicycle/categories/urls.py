from django.urls import path
from .views import category_list, category_create, category_update, category_delete

urlpatterns = [
    path('', category_list, name='category_list'),
    path('add/', category_create, name='category_create'),
    path('edit/<int:pk>/', category_update, name='category_update'),
    path('delete/<int:pk>/', category_delete, name='category_delete'),
]
