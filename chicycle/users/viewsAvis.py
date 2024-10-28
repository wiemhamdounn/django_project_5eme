from django.shortcuts import render, redirect, get_object_or_404
from .forms import AvisForm
from django.contrib.auth.decorators import login_required
from .models import Reponse, Avis
from .forms import ReponseForm
from django.contrib import messages
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from transformers import logging
import os

logging.set_verbosity_error()  # Désactiver les avertissements liés aux logs transformers

# Chemin de cache pour les modèles pré-entraînés
MODEL_PATH = "gpt2"

# Fonction pour charger le modèle GPT-2 de façon sécurisée
def load_gpt2_model():
    try:
        # Charger le modèle et le tokenizer GPT-2
        model = AutoModelForCausalLM.from_pretrained(MODEL_PATH)
        tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
        return pipeline('text-generation', model=model, tokenizer=tokenizer)
    except Exception as e:
        print(f"Erreur lors du chargement du modèle GPT-2 : {e}")
        return None

# Charger le modèle GPT-2
response_generator = load_gpt2_model()

# Si le modèle est chargé avec succès, continuer le traitement
if response_generator:
    print(response_generator("This is a test", max_length=50))
else:
    print("Le modèle GPT-2 n'a pas pu être chargé.")

def creer_avis(request):
    if request.method == 'POST':
        form = AvisForm(request.POST)
        if form.is_valid():
            avis = form.save(commit=False)
            avis.utilisateur = request.user  # Lier l'avis à l'utilisateur connecté
            avis.save()

         
            if avis.sentiment == 'Positive':
                messages.success(request, 'Thank you for your positive feedback! 😊 We''re glad you had a great experience.')
            elif avis.sentiment == 'Neutral':
                messages.info(request, 'Thank you for your feedback! 😐 We''re always looking to improve.')
            elif avis.sentiment == 'Negative':
                messages.warning(request, 'We''re sorry to hear about your experience. 😔 We''ll strive to do better next time.')
            #  messages.success(request, 'Votre avis a bien été ajouté !')

            return redirect('user_avis')  # Rediriger vers la liste des avis de l'utilisateur
    else:
        form = AvisForm()

    return render(request, 'avis/creer_avis.html', {'form': form})


def modifier_avis(request, avis_id):
    # On récupère l'avis basé uniquement sur l'ID, sans vérifier l'utilisateur
    
    avis = get_object_or_404(Avis, id=avis_id)
    
    # Gestion du formulaire POST pour la soumission des modifications
    if request.method == 'POST':
        form = AvisForm(request.POST, instance=avis)
        if form.is_valid():
            form.save()
            return redirect('liste_avis')  # Redirige vers la liste des avis après modification
    else:
        form = AvisForm(instance=avis)
    
    return render(request, 'avis/modifier_avis.html', {'form': form})

@login_required
def supprimer_avis(request, avis_id):
    avis = get_object_or_404(Avis, id=avis_id)
    if request.method == 'POST':
        avis.delete()
        return redirect('liste_avis')
    return render(request, 'avis/supprimer_avis.html', {'avis': avis})
def liste_avis(request):
    avis = Avis.objects.all() 
    
    # Extraire les produits et leurs évaluations
    products = [avis_item.produit for avis_item in avis]
    ratings = [avis_item.note for avis_item in avis]

    context = {
        'avis': avis,
        'products': products,
        'ratings': ratings
    }
    
    return render(request, 'avis/liste_avis.html', context)  # Correction du contexte


def detail_avis(request, avis_id):
    avis = get_object_or_404(Avis, id=avis_id)
    reponses = avis.reponses.all()  # Récupère toutes les réponses liées à cet avis
    return render(request, 'avis/detail_avis.html', {'avis': avis, 'reponses': reponses})
def user_avis(request):
    avis_list = Avis.objects.filter(utilisateur=request.user)  # Récupérer uniquement les avis de l'utilisateur connecté
    context = {
        'avis_list': avis_list
    }
    return render(request, 'avis/user_avis.html', context)

@login_required
# def creer_reponse(request, avis_id):
#     avis = get_object_or_404(Avis, id=avis_id)
#     print(f"User authenticated: {request.user.is_authenticated}")  # Vérifie si l'utilisateur est connecté
    
#     if request.method == 'POST':
#         form = ReponseForm(request.POST)
#         print(f"Form is valid: {form.is_valid()}")  # Affiche si le formulaire est validé
#         if form.is_valid():
#             reponse = form.save(commit=False)
#             reponse.avis = avis
#             reponse.utilisateur = request.user
#             reponse.save()
#             print("Response saved successfully")  # Log si la réponse est bien enregistrée
#             return redirect('detail_avis', avis_id=avis.id)
#         else:
#             # Afficher les erreurs de validation dans la console
#             print("Form errors: ", form.errors)
#     else:
#         form = ReponseForm()

#     return render(request, 'reponse/creer_reponse.html', {'form': form, 'avis': avis})


@login_required

def creer_reponse(request, avis_id):
    avis = get_object_or_404(Avis, id=avis_id)
    
    # Générer une suggestion spécifique en fonction du sentiment de l'avis
    if avis.sentiment == 'Positive':
        suggestion = "Thank you for your feedback! We're glad you had a great experience with our product."
    elif avis.sentiment == 'Neutral':
        suggestion = "Thank you for your feedback. We appreciate your input and will continue to improve."
    elif avis.sentiment == 'Negative':
        suggestion = "We're sorry to hear about your experience. We're committed to improving and will address this issue as soon as possible."
    else:
        suggestion = "Thank you for your feedback."

    if request.method == 'POST':
        form = ReponseForm(request.POST)
        if form.is_valid():
            reponse = form.save(commit=False)
            reponse.avis = avis
            reponse.utilisateur = request.user
            reponse.save()
            return redirect('detail_avis', avis_id=avis.id)
        else:
            print("Form errors: ", form.errors)
    else:
        # Pré-remplir le champ commentaire avec la suggestion
        form = ReponseForm(initial={'commentaire': suggestion})

    return render(request, 'reponse/creer_reponse.html', {'form': form, 'avis': avis, 'suggestion': suggestion})

       


@login_required
def modifier_reponse(request, reponse_id):
    reponse = get_object_or_404(Reponse, id=reponse_id, utilisateur=request.user)
    if request.method == 'POST':
        form = ReponseForm(request.POST, instance=reponse)
        if form.is_valid():
            form.save()
            return redirect('detail_avis', avis_id=reponse.avis.id)
    else:
        form = ReponseForm(instance=reponse)
    return render(request, 'reponse/modifier_reponse.html', {'form': form, 'reponse': reponse})
@login_required
def supprimer_reponse(request, reponse_id):
    reponse = get_object_or_404(Reponse, id=reponse_id, utilisateur=request.user)
    if request.method == 'POST':
        reponse.delete()
        return redirect('detail_avis', avis_id=reponse.avis.id)
    return render(request, 'reponse/supprimer_reponse.html', {'reponse': reponse})

