from django.shortcuts import render, redirect
from .models import Produit
from .forms import ProduitForm
from django.contrib import messages
from .ai_model import *
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q


def liste_produits(request):
    produits = Produit.objects.all()
    paginator = Paginator(produits, 4)  # Affiche 10 produits par page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'produit/liste_produits.html', {'produits': page_obj})

def ajouter_produit(request):
    if request.method == 'POST':
        form = ProduitForm(request.POST , request.FILES)
        if form.is_valid():
            form.save()
            return redirect('liste_produits')
    else:
        form = ProduitForm()
    return render(request, 'produit/ajouter_produit.html', {'form': form})

def predire_prix(request):
    prix_predite = None  # Initialiser la variable pour le prix prédit
    message = None
    prix_pre = None
    nouveau_produit_data = {
            'type': None,
            'couleur': None,
            'taille': None,
            'genre': None,
        }
    if request.method == 'POST':
        # Récupérer les données du formulaire
        type_produit = request.POST.get('type')
        couleur = request.POST.get('couleur')
        taille = request.POST.get('taille')
        genre = request.POST.get('genre')

        # Créer un dictionnaire pour la prédiction
        nouveau_produit_data = {
            'type': type_produit,
            'couleur': couleur,
            'taille': taille,
            'genre': genre,
        }

        # Faire la prédiction
        message , prix_predite = create_pipeline(nouveau_produit_data)
        prix_pre = prix_predite[0]

    return render(request, 'produit/predire_prix.html', {'message': message , 'prix_predite': prix_pre , 'nouveau_produit_data': nouveau_produit_data})

def modifier_produit(request, id):
    produit = Produit.objects.get(id=id)
    if request.method == 'POST':
        form = ProduitForm(request.POST,request.FILES, instance=produit  )
        if form.is_valid():
            form.save()
            return redirect('liste_produits')
    else:
        form = ProduitForm(instance=produit)
    return render(request, 'produit/modifier_produit.html', {'form': form})

def delete_produit(request, id):
    produit = get_object_or_404(Produit, id=id)
    if request.method == 'POST':
        produit.delete()
        return redirect('liste_produits')
    return render(request, 'produit/delete_produit.html', {'produit': produit})


def add_product_view(request):
    prix_predite = None 
    if request.method == 'POST':
        form = ProduitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_produits')  # Rediriger vers la liste des produits

    else:
        # Récupérer les données du formulaire d'ajout
        type_produit = request.GET.get('type')
        couleur = request.GET.get('couleur')
        taille = request.GET.get('taille')
        genre = request.GET.get('genre')
        prix_predite = request.GET.get('prix_predite')  # Récupérer le prix prédit

  

        # Remplir le formulaire avec les données pré-remplies
        initial_data = {
            'type': type_produit,
            'couleur': couleur,
            'taille': taille,
            'genre': genre,
            'prix': prix_predite
        }
        form = ProduitForm(initial=initial_data)

    return render(request, 'produit/add_product_form.html', {'form': form  })


# user 

def liste_produits_user(request):
    # Récupération des paramètres de recherche et de tri
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    size_filter = request.GET.get('size', '')
    sort_by = request.GET.get('sort', '')

    # Filtrer les produits en fonction des paramètres
    produits = Produit.objects.all()

    if search_query:
        produits = produits.filter(Q(nom__icontains=search_query) | Q(type__icontains=search_query))

    if category_filter:
        produits = produits.filter(category__name=category_filter)

    if size_filter:
        produits = produits.filter(taille=size_filter)

    # Appliquer le tri
    if sort_by == 'price':
        produits = produits.order_by('prix')
    elif sort_by == 'category':
        produits = produits.order_by('category__name')
    elif sort_by == 'size':
        produits = produits.order_by('taille')

    # Pagination
    paginator = Paginator(produits, 10)  # Affiche 10 produits par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Récupérer les valeurs uniques pour les filtres
    categories = Produit.objects.values_list('category__name', flat=True).distinct()
    tailles = Produit.objects.values_list('taille', flat=True).distinct()

    return render(request, 'produit/list_product-user.html', {
        'produits': page_obj,
        'search_query': search_query,
        'category_filter': category_filter,
        'size_filter': size_filter,
        'sort_by': sort_by,
        'categories': categories,
        'tailles': tailles,
    })