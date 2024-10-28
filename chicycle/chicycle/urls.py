from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView
from users import views
from users import viewsBlog  # Importation des vues du blog
from django.conf import settings
from django.conf.urls.static import static

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
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
