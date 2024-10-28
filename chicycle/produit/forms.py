from django import forms
from .models import Produit

class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = ['nom', 'type', 'couleur', 'taille', 'genre', 'description', 'prix', 'stock', 'image', 'category']
