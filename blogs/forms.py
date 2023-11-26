from django import forms
from .models import Blog


class BlogPostForm(forms.ModelForm):

    class Meta:
        model = Blog
        fields = ('image', 'title', 'content', 'createdAt')
        widgets = {
            'image': forms.ClearableFileInput(attrs={'id': 'id_image'}),
            'title': forms.TextInput(attrs={'id': 'id_title'}),
            'content': forms.Textarea(attrs={'id': 'id_content'}),
            'createdAt': forms.TextInput(attrs={'id': 'id_createdAt'}),
        }
        # exclude = ['published_date']