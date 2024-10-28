from django.shortcuts import render, get_object_or_404, redirect
from .models import Category
from .forms import CategoryForm
from django.core.paginator import Paginator



# Liste des catégories
def category_list(request):
    categories = Category.objects.all()
    paginator = Paginator(categories, 4) 

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'categories/category_list.html', {'categories': page_obj})

# Ajouter une nouvelle catégorie
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')  # Rediriger vers la liste des catégories
    else:
        form = CategoryForm()
    return render(request, 'categories/category_form.html', {'form': form})

# Modifier une catégorie
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')  # Rediriger vers la liste des catégories
    else:
        form = CategoryForm(instance=category)
    return render(request, 'categories/category_form.html', {'form': form})

# Supprimer une catégorie
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')  # Rediriger vers la liste des catégories
    return render(request, 'categories/category_confirm_delete.html', {'category': category})
