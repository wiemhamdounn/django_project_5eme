from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from transformers import MarianMTModel, MarianTokenizer

class CustomUser(AbstractUser):
    ROLES = (
        ('superadmin', 'Super Admin'),
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=10, choices=ROLES, default='user')
    image = models.ImageField(upload_to='profile_images/', default='profile_images/default.png', blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)


class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    title_en = models.CharField(max_length=255, blank=True, null=True)  # Champ pour le titre en anglais
    content_en = models.TextField(blank=True, null=True)  # Champ pour le contenu en anglais
    summary = models.TextField(blank=True, null=True)  # Résumé automatique
    tags = models.TextField(blank=True, null=True)  # Champ pour stocker les balises
    excerpt = models.TextField(blank=True, null=True)  # Nouveau champ pour l'extrait

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    