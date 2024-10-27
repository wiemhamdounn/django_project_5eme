from django.shortcuts import render, get_object_or_404, redirect
from .models import BlogPost
from .forms import BlogPostForm
from django.contrib import messages
from transformers import MarianMTModel, MarianTokenizer
from transformers import BartForConditionalGeneration, BartTokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from keybert import KeyBERT
from rake_nltk import Rake


# Liste des articles (Read)
def list_blogs(request):
    posts = BlogPost.objects.all().order_by('-created_at')
    return render(request, 'blog-management/blog_list.html', {'posts': posts})

# Détail d'un article (Read)
def blog_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    return render(request, 'blog-management/blog_detail.html', {'post': post})

# # Créer un nouvel article (Create)
# def blog_create(request):
#     if request.method == 'POST':
#         form = BlogPostForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Article créé avec succès.')
#             return redirect('list_blogs')
#     else:
#         form = BlogPostForm()

#     return render(request, 'blog-management/blog_form.html', {'form': form})
def blog_create(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            # Créer une instance de l'article sans la sauvegarder immédiatement
            post = form.save(commit=False)
            
            # Générer l'extrait à partir du contenu
            post.excerpt = generate_excerpt(post.content)
            
            # Ensuite, sauvegarder l'article avec l'extrait
            post.save()
            
            messages.success(request, 'Article créé avec succès avec extrait généré automatiquement.')
            return redirect('list_blogs')
    else:
        form = BlogPostForm()

    return render(request, 'blog-management/blog_form.html', {'form': form})



# # Mettre à jour un article (Update)
def blog_update(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Article mis à jour avec succès.')
            return redirect('blog_detail', pk=pk)
    else:
        form = BlogPostForm(instance=post)

    return render(request, 'blog-management/blog_form.html', {'form': form})

# Supprimer un article (Delete)
def blog_delete(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Article supprimé avec succès.')
        return redirect('list_blogs')
    return render(request, 'blog-management/blog_confirm_delete.html', {'post': post})


def generate_excerpt(content, word_limit=50):
    """
    Génère un extrait automatique à partir des premiers mots du contenu.
    """
    words = content.split()  # Séparer le contenu en mots
    if len(words) > word_limit:
        excerpt = " ".join(words[:word_limit]) + "..."
    else:
        excerpt = content  # Si le contenu est plus court que la limite, on prend tout
    return excerpt

def generate_excerpt_view(request, post_id):
    """
    Vue pour générer un extrait automatique pour un article spécifique.
    """
    post = get_object_or_404(BlogPost, id=post_id)

    try:
        # Utilisation de la fonction generate_excerpt pour créer un extrait
        post.excerpt = generate_excerpt(post.content)
        post.save()
        messages.success(request, 'Extrait généré avec succès.')
    except Exception as e:
        messages.error(request, f'Erreur lors de la génération de l\'extrait : {e}')
    
