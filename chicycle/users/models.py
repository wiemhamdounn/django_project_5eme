from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from transformers import MarianMTModel, MarianTokenizer
from django.conf import settings

class CustomUser(AbstractUser):
    ROLES = (
        ('superadmin', 'Super Admin'),
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=10, choices=ROLES, default='user')
    image = models.ImageField(upload_to='profile_images/', default='profile_images/default.png', blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    
    # Points d'activité pour l'utilisateur
    points = models.IntegerField(default=0)  # Assurez-vous que cette ligne est correctement indentée

    # Badge attribué à l'utilisateur en fonction de ses activités
    badge = models.CharField(max_length=50, blank=True, null=True)

class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    title_en = models.CharField(max_length=255, blank=True, null=True)
    content_en = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    tags = models.TextField(blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    excerpt = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Générer un résumé automatiquement s'il est vide
        if not self.summary and self.content:
            self.summary = self.content[:150] + "..."  # Prendre les 150 premiers caractères
        super().save(*args, **kwargs)

    

