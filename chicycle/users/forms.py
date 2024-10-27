from django import forms
from .models import CustomUser
from .models import BlogPost



class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'role']
class UpdateProfileImageForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content']