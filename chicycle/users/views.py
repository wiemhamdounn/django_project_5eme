from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required,  user_passes_test
from .forms import RegisterForm
from django.contrib import messages
from .models import CustomUser
from .forms import UpdateProfileImageForm
from PIL import Image, ImageDraw
import random
import subprocess
from django.conf import settings
import os
import io
import requests
from django.core.files.base import ContentFile
from django.dispatch import receiver
from django.db.models.signals import post_save

failed_attempts = {}

def login_view(request):
    global failed_attempts

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if username in failed_attempts and failed_attempts[username] >= 5:
            return redirect('failure')

        if user is not None:
            if user.is_active:
                login(request, user)
                
                # Reset failed attempts on successful login
                if username in failed_attempts:
                    del failed_attempts[username]

                # Redirect based on user role
                if user.role == 'admin':
                    return redirect('admin_dashboard')
                else:
                    return redirect('user_dashboard')
            else:
                messages.error(request, 'Votre compte est désactivé.')
        else:
            # Increment failed attempts if authentication fails
            if username in failed_attempts:
                failed_attempts[username] += 1
            else:
                failed_attempts[username] = 1

            # Display error message with remaining attempts
            messages.error(request, f'Identifiants incorrects. Tentative {failed_attempts[username]}/5.')

            # Redirect to failure page after 5 attempts
            if failed_attempts[username] >= 5:
                return redirect('failure')

    return render(request, 'login.html')
def failure(request):
    return render(request, 'failure.html')
@login_required
def admin_dashboard(request):
    return render(request, 'admin/admin_dashboard.html')


@login_required
def user_dashboard(request):
    return render(request, 'user/user_dashboard.html')




def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hacher le mot de passe
            user.save()
            login(request, user)
            # Redirection après inscription selon le rôle
            if user.role == 'superadmin':
                return redirect('superadmin_dashboard')
            elif user.role == 'admin':
                return redirect('admin_dashboard')
            else:
                return redirect('user_dashboard')
    else:
        form = RegisterForm()


    return render(request, 'register.html', {'form': form})
# Vérifie si l'utilisateur est admin ou superadmin
def is_admin(user):
    return user.role in ['admin']

def is_user(user):
    return user.role in ['user']

# Liste de tous les utilisateurs (admin et superadmin seulement)
@login_required
@user_passes_test(is_admin)
def get_all_users(request):
    users = CustomUser.objects.all()
    return render(request, 'user-management/users.html', {'users': users})


@login_required
@user_passes_test(is_admin)
def update_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
   
    if request.method == 'POST':
        # Utiliser le formulaire existant mais sans le champ mot de passe pour la mise à jour
        form = RegisterForm(request.POST, instance=user)
        form.fields.pop('password')  # Supprime le champ mot de passe pour ne pas le mettre à jour
       
        if form.is_valid():
            # Enregistrer les autres champs sans changer le mot de passe
            form.save()
            messages.success(request, 'Utilisateur mis à jour avec succès.')
            return redirect('get_all_users')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = RegisterForm(instance=user)
        form.fields.pop('password')  # Supprime le champ mot de passe en mode GET pour la mise à jour


    return render(request, 'user-management/update_user.html', {'form': form, 'user': user})
# Bannir un utilisateur (désactiver)
@login_required
@user_passes_test(is_admin)
def ban_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_active = False  # Désactiver l'utilisateur (ban)
    user.save()
    messages.success(request, 'Utilisateur banni.')
    return redirect('get_all_users')


# Débannir un utilisateur (activer)
@login_required
@user_passes_test(is_admin)
def unban_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_active = True  # Activer l'utilisateur (unban)
    user.save()
    messages.success(request, 'Utilisateur débanni.')
    return redirect('get_all_users')



@login_required
@user_passes_test(is_user)

def user_profile(request):
    user = request.user

    # Gérer le formulaire de mise à jour de l'image pour les utilisateurs normaux
    if request.method == 'POST':
        form = UpdateProfileImageForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_profile')  # Redirection après la soumission du formulaire
    else:
        form = UpdateProfileImageForm(instance=user)

    # Rendre le template pour les utilisateurs normaux
    return render(request, 'user-management/user_profile.html', {
        'user': user, 
        'form': form
    })

@login_required
@user_passes_test(is_admin)
def admin_profile(request):
    user = request.user
    # Gérer le formulaire de mise à jour de l'image pour les administrateurs
    if request.method == 'POST':
        form = UpdateProfileImageForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('admin_profile')  # Redirection après la soumission du formulaire
    else:
        form = UpdateProfileImageForm(instance=user)

    # Rendre le template pour les administrateurs
    return render(request, 'user-management/admin_profile.html', {
        'user': user, 
        'form': form
    })

@login_required
@login_required
def generate_ai_avatar_view(request):
    user = request.user
    try:
        # Utiliser RoboHash pour générer un avatar IA basé sur le nom d'utilisateur
        avatar_url = f'https://robohash.org/{user.username}.png'

        # Faire la requête HTTP pour récupérer l'image de l'avatar
        response = requests.get(avatar_url)
        if response.status_code == 200:
            # Sauvegarder l'avatar généré dans le champ avatar de l'utilisateur
            user.avatar.save(f'avatar_{user.username}.png', ContentFile(response.content), save=True)
            messages.success(request, "Avatar IA généré avec succès.")
        else:
            messages.error(request, "Impossible de générer l'avatar à partir de l'IA.")
    except Exception as e:
        messages.error(request, f"Une erreur s'est produite lors de la génération de l'avatar IA : {str(e)}")

    # Redirection en fonction du rôle
    if user.role == 'admin':
        return redirect('admin_profile')  # Redirection vers la page admin
    elif user.role == 'user':
        return redirect('user_profile')  # Redirection vers la page utilisateur
    else:
        return redirect('home')