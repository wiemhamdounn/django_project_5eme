

from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView
from users import views
from users import viewsBlog  # Importation des vues du blog
from django.conf import settings
from django.conf.urls.static import static
from users.viewsAvis import creer_avis, modifier_avis, supprimer_avis, liste_avis ,user_avis,detail_avis ,creer_reponse,modifier_reponse,supprimer_reponse

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('register/', views.register_view, name='register'),  # URL d'inscription

    path('profile/user/', views.user_profile, name='user_profile'),
    path('profile/admin/', views.admin_profile, name='admin_profile'),
    path('generate-ai-avatar/', views.generate_ai_avatar_view, name='generate_ai_avatar'),
    path('logout/', LogoutView.as_view(), name='logout'),  # URL pour la déconnexion

    # Gestion des utilisateurs
    path('users/', views.get_all_users, name='get_all_users'),
    path('users/update/<int:user_id>/', views.update_user, name='update_user'),
    path('users/ban/<int:user_id>/', views.ban_user, name='ban_user'),
    path('users/unban/<int:user_id>/', views.unban_user, name='unban_user'),

    # Gestion des articles de blog avec viewsBlog
    path('post/listPost', viewsBlog.list_blogs, name='list_blogs'),  # Liste des articles
    path('post/<int:pk>/', viewsBlog.blog_detail, name='blog_detail'),  # Détail d'un article
    path('post/new/', viewsBlog.blog_create, name='blog_create'), # Créer un article
    path('post/<int:pk>/edit/', viewsBlog.blog_update, name='blog_update'),  # Modifier un article
    path('post/<int:pk>/delete/', viewsBlog.blog_delete, name='blog_delete'), # Supprimer un article
    path('post/<int:post_id>/generate_excerpt/', viewsBlog.generate_excerpt_view, name='generate_excerpt'),
    path('failure/', views.failure, name='failure'),  # Page d'échec



    
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

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
