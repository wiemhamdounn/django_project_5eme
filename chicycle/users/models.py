from django.contrib.auth.models import AbstractUser
from django.db import models
from textblob import TextBlob
from flask import Flask, request, jsonify
import requests
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
from django.conf import settings
from django.core.exceptions import ValidationError

nltk.download('vader_lexicon')
class CustomUser(AbstractUser):
    ROLES = (
        ('superadmin', 'Super Admin'),
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=10, choices=ROLES, default='user')


# class Avis(models.Model):
    
    # utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # produit = models.ForeignKey('Produit', on_delete=models.CASCADE)  # Relier à un modèle Produit
    # utilisateur = models.CharField(max_length=255)
    # produit = models.CharField(max_length=255)
    # commentaire = models.TextField()
    # note = models.IntegerField()
    # date_creation = models.DateTimeField(auto_now_add=True)
    # sentiment = models.CharField(max_length=50, null=True, blank=True)  # Champ pour stocker le sentiment

    # def save(self, *args, **kwargs):
        # Analyse de sentiment avec TextBlob
        # blob = TextBlob(self.commentaire)
        # polarity = blob.sentiment.polarity

        # Détermine le sentiment basé sur la polarité
    #     if polarity > 0:
    #         self.sentiment = 'Positive'
    #     elif polarity < 0:
    #         self.sentiment = 'Negative'
    #     else:
    #         self.sentiment = 'Neutral'

    #     super(Avis, self).save(*args, **kwargs)

    # def __str__(self):
    #     return f"Avis de {self.utilisateur} sur {self.produit}"

class Produit(models.Model):
    nom = models.CharField(max_length=255)
    utilisateur = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Le propriétaire du produit

    def __str__(self):
        return f"{self.nom} (Propriétaire: {self.utilisateur.username})"

class Avis(models.Model):
    utilisateur = models.CharField(max_length=255)
    produit = models.CharField(max_length=255)
    commentaire = models.TextField()
    note = models.IntegerField()
    date_creation = models.DateTimeField(auto_now_add=True)
    sentiment = models.CharField(max_length=50, null=True, blank=True)

    def clean(self):
        if self.note is None or not (1 <= self.note <= 5):
            raise ValidationError('The rating must be between 1 and 5.')
        if not self.commentaire or len(self.commentaire) < 5:
            raise ValidationError('The comment must be at least 5 characters long.')

    def save(self, *args, **kwargs):
        # Analyser le commentaire avec VADER
        analyser = SentimentIntensityAnalyzer()
        sentiment_score = analyser.polarity_scores(self.commentaire)
        
        # Utiliser le score de polarité pour déterminer le sentiment
        if sentiment_score['compound'] > 0.05:
            self.sentiment = 'Positive'
        elif sentiment_score['compound'] < -0.05:
            self.sentiment = 'Negative'
        else:
            self.sentiment = 'Neutral'

        super(Avis, self).save(*args, **kwargs)

    def __str__(self):
        return f"Avis de {self.utilisateur} sur {self.produit}"


class Reponse(models.Model):
    avis = models.ForeignKey(Avis, on_delete=models.CASCADE, related_name='reponses')
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    commentaire = models.TextField()  # Champ pour la réponse
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Réponse de {self.utilisateur} sur {self.avis}"
