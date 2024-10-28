from django.db import models
from categories.models import Category 


class Produit(models.Model):
    nom = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    couleur = models.CharField(max_length=255)
    taille = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    image = models.ImageField(upload_to='images/', blank=True, null=True)  # Stocke l'image dans media/images/
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)



    def __str__(self):
        return self.nom
