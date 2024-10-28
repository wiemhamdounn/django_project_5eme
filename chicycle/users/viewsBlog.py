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
from .views import update_user_badge_and_role
from transformers import pipeline
classifier = pipeline("text-classification", model="unitary/toxic-bert")


# Liste des articles (Read)
def list_blogs(request):
    posts = BlogPost.objects.all().order_by('-created_at')
    return render(request, 'blog-management/blog_list.html', {'posts': posts})

# Détail d'un article (Read)
def blog_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    return render(request, 'blog-management/blog_detail.html', {'post': post})
def blog_create(request):
    offensive_message = None  # Variable pour stocker le message offensant
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            
            # Vérifier si le contenu contient des mots offensants
            result = classifier(post.content)
            for prediction in result:
                label = prediction['label']
                score = prediction['score']
                
                if label == 'toxic' and score > 0.5:  # Ajustez le seuil si nécessaire
                    offensive_message = f"Le contenu est toxique avec un score de {score:.2f}."
                    messages.error(request, offensive_message)
                    return render(request, 'blog-management/blog_form.html', {'form': form, 'offensive_message': offensive_message})

            post.excerpt = generate_excerpt(post.content)  # Génération de l'extrait
            post.save()

            # Ajouter des points pour l'utilisateur
            request.user.points += 10  # Ajouter 10 points pour chaque article publié
            request.user.save()

            # Mettre à jour le badge et le rôle en fonction des nouveaux points
            update_user_badge_and_role(request.user)

            messages.success(request, 'Article créé avec succès.')
            return redirect('list_blogs')
    else:
        form = BlogPostForm()

    return render(request, 'blog-management/blog_form.html', {'form': form, 'offensive_message': offensive_message})






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
    
def detect_offensive_language(text):
    result = classifier(text)
    print(f"Resultat pour '{text}': {result}")  # Ajoutez cette ligne pour le débogage
    for prediction in result:
        label = prediction['label']
        score = prediction['score']
        print(f"Label: {label}, Score: {score}")  # Débogage
        if label == 'TOXIC' and score > 0.5:  # Ajustez le seuil si nécessaire
            return True  # Texte offensant détecté
    return False  # Aucun langage offensant détecté

# Tester avec des phrases
test_phrases = [
    "Ce texte contient un mot comme idiot.",
    "Vous êtes vraiment un imbécile.",
    "C'est un bon article sans mauvais langage.",
    "Ce n'est pas bien de dire des gros mots comme putain.",
    "Je pense que ce terme est raciste.",
    "Tout va bien ici, rien de toxique.",
    "Allez vous faire foutre, c'est inacceptable !"
]

for phrase in test_phrases:
    if detect_offensive_language(phrase):
        print(f"Offensant : {phrase}")
    else:
        print(f"Propre : {phrase}")