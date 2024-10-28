
"""
URL configuration for chicycle project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView
from users import views
from users.viewsAvis import creer_avis, modifier_avis, supprimer_avis, liste_avis ,user_avis,detail_avis ,creer_reponse,modifier_reponse,supprimer_reponse

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),
    path('superadmin_dashboard/', views.superadmin_dashboard, name='superadmin_dashboard'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('register/', views.register_view, name='register'),  # URL d'inscription
    path('logout/', LogoutView.as_view(), name='logout'),  # URL pour la déconnexion
    
    path('creer/', creer_avis, name='creer_avis'),
    path('modifier/<int:avis_id>/', modifier_avis, name='modifier_avis'),
    path('supprimer/<int:avis_id>/', supprimer_avis, name='supprimer_avis'),
    path('mes-avis/', user_avis, name='user_avis'),
            # Routes pour les réponses
    path('avis/<int:avis_id>/reponse/creer/', creer_reponse, name='creer_reponse'),
    path('reponse/<int:reponse_id>/modifier/', modifier_reponse, name='modifier_reponse'),
    path('reponse/<int:reponse_id>/supprimer/', supprimer_reponse, name='supprimer_reponse'),
    path('liste/', liste_avis, name='liste_avis'), 
    path('avis/<int:avis_id>/', detail_avis, name='detail_avis'),
    path('users/', views.get_all_users, name='get_all_users'),  # URL pour la gestion des utilisateurs
    path('users/update/<int:user_id>/', views.update_user, name='update_user'),  # URL pour mettre à jour un utilisateur
    path('users/ban/<int:user_id>/', views.ban_user, name='ban_user'),  # URL pour bannir un utilisateur
    path('users/unban/<int:user_id>/', views.unban_user, name='unban_user'),  # URL pour débannir un utilisateur


]
