import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from .models import Produit
import numpy as np

# Crée un pipeline de modèle ML avec les données de la base de données
def create_pipeline(nouveau_produit_data):
    # Récupérer les produits existants pour entraîner le modèle
    produits = Produit.objects.all().values('type', 'couleur', 'taille', 'genre', 'prix')
    df = pd.DataFrame(produits)

    if df.empty:
        return None  # S'assurer qu'il y a des données

    # Séparer les caractéristiques (X) et la cible (y)
    X = df[['type', 'couleur', 'taille', 'genre']]
    y = df['prix']

    # Encoder les variables catégoriques
    encoder = OneHotEncoder(handle_unknown='ignore')
    X_encoded = encoder.fit_transform(X)

    # Créer et entraîner le modèle
    model = RandomForestRegressor()
    model.fit(X_encoded, y)

    # Calculer le score de confiance du modèle
    score_confiance = model.score(X_encoded, y)

    
    # Encoder les données du nouveau produit
    nouveau_produit_df = pd.DataFrame([nouveau_produit_data])
    nouveau_produit_encoded = encoder.transform(nouveau_produit_df)

    valeurs_connues = [
        set(df['type'].unique()),
        set(df['couleur'].unique()),
        set(df['taille'].unique()),
        set(df['genre'].unique())
    ]
    valeurs_nouveau_produit = [
        nouveau_produit_data.get('type', None),
        nouveau_produit_data.get('couleur', None),
        nouveau_produit_data.get('taille', None),
        nouveau_produit_data.get('genre', None)
    ]
    for idx, valeur in enumerate(valeurs_nouveau_produit):
        if valeur not in valeurs_connues[idx]:
            score_confiance *= 0.6  # Diminuer la confiance de moitié si une valeur inconnue est détectée

    # Faire la prédiction
    prix_predite = model.predict(nouveau_produit_encoded)
    
    if score_confiance < 0.3:
        message= f"La prédiction du prix est : {prix_predite[0]:.2f}. Attention : la confiance est faible 🔴 ({score_confiance * 100:.2f}%)"
    elif score_confiance < 0.5:
        message= f"La prédiction du prix est : {prix_predite[0]:.2f}. Attention : la confiance est faible 🟠 ({score_confiance * 100:.2f}%)"
    elif score_confiance < 0.7:
        message= f"La prédiction du prix est : {prix_predite[0]:.2f}. la confiance est acceptable 🟡 ({score_confiance * 100:.2f}%)"
    else:
        message= f"La prédiction du prix est : {prix_predite[0]:.2f}. Confiance 🟢 : {score_confiance * 100:.2f}%"
    
    return message,prix_predite

  

# Fonction de prédiction pour un nouveau produit
# def predict_price(nouveau_produit_data):
#     pipeline = create_pipeline()
#     nouveau_produit = pd.DataFrame([nouveau_produit_data])
#     prix_predite = pipeline.predict(nouveau_produit)
#     return prix_predite[0]
