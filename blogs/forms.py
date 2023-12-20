from django import forms
from .models import Blogs


class BlogPostForm(forms.ModelForm):

    class Meta:
        model = Blogs
        fields = ('image', 'title', 'content', 'created_at', 'last_updated')
        widgets = {
            'image': forms.ClearableFileInput(attrs={'id': 'id_image'}),
            'title': forms.TextInput(attrs={'id': 'id_title'}),
            'content': forms.Textarea(attrs={'id': 'id_content'}),
            'created_at': forms.TextInput(attrs={'id': 'id_createdAt'}),
            'last_updated': forms.TextInput(attrs={'id': 'id_last_updated'}),
        }
        # exclude = ['published_date']