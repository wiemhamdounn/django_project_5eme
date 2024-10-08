from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required,  user_passes_test
from .forms import RegisterForm
from django.contrib import messages
from .models import CustomUser




def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)


        if user is not None:
            if user.is_active:
                login(request, user)
                # Redirection basée sur le rôle de l'utilisateur
                if user.role == 'superadmin':
                    return redirect('superadmin_dashboard')
                elif user.role == 'admin':
                    return redirect('admin_dashboard')
                else:
                    return redirect('user_dashboard')
            else:
                messages.error(request, 'Votre compte est désactivé.')
        else:
            messages.error(request, 'Identifiants incorrects.')


    return render(request, 'login.html')


@login_required
def superadmin_dashboard(request):
    return render(request, 'super-admin/superadmin_dashboard.html')


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
def is_admin_or_superadmin(user):
    return user.role in ['admin', 'superadmin']


# Liste de tous les utilisateurs (admin et superadmin seulement)
@login_required
@user_passes_test(is_admin_or_superadmin)
def get_all_users(request):
    users = CustomUser.objects.all()
    return render(request, 'user-management/users.html', {'users': users})


@login_required
@user_passes_test(is_admin_or_superadmin)
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
@user_passes_test(is_admin_or_superadmin)
def ban_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_active = False  # Désactiver l'utilisateur (ban)
    user.save()
    messages.success(request, 'Utilisateur banni.')
    return redirect('get_all_users')


# Débannir un utilisateur (activer)
@login_required
@user_passes_test(is_admin_or_superadmin)
def unban_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_active = True  # Activer l'utilisateur (unban)
    user.save()
    messages.success(request, 'Utilisateur débanni.')
    return redirect('get_all_users')

