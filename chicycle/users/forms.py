from django import forms
from .models import CustomUser
from .models import Avis
from .models import Reponse
from django.core.exceptions import ValidationError
class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'role']


class AvisForm(forms.ModelForm):
    class Meta:
        model = Avis
        fields = ['produit', 'commentaire', 'note']
        widgets = {
            'note': forms.HiddenInput(),  
        }

    def clean_commentaire(self):
        commentaire = self.cleaned_data.get('commentaire')
        if len(commentaire) < 4:
            raise ValidationError('The comment must contain at least 4 characters.')
        return commentaire

class ReponseForm(forms.ModelForm):
    class Meta:
        model = Reponse
        fields = ['commentaire']
    def clean_commentaire(self):
        commentaire = self.cleaned_data.get('commentaire')
        if len(commentaire) < 5:
            raise ValidationError('The response must contain at least 5 characters.')
        return commentaire