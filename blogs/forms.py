from django import forms
from blogs.models import Category, Post
from django_summernote.widgets import SummernoteWidget

class BlogSearchForm(forms.Form):
    search = forms.CharField(required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'tags')
        widgets = {
            'content': SummernoteWidget()
        }

class PostEditForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ('title', 'content', 'tags')
        widgets = {
            'content': SummernoteWidget()
        }

