from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.liste_produits, name='liste_produits'),
    path('ajouter/', views.ajouter_produit, name='ajouter_produit'),
    path('produits/update/<int:id>/', views.modifier_produit, name='update_produit'),
    path('produits/delete/<int:id>/', views.delete_produit, name='delete_produit'),
    path('produits/predire/', views.predire_prix, name='predire_prix'),
    path('produits/ajouter/', views.add_product_view, name='add_product_view'),
    path('user-product/', views.liste_produits_user, name='liste_produits_user'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)