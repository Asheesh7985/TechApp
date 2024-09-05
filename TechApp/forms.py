from django import forms
from .models import Post, Category
from froala_editor.widgets import FroalaEditor

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=FroalaEditor)
    class Meta:
        model = Post
        fields = ['title','content','slug','category','author','image']
        labels = {'title':'Title','content':'Content','slug':'Slug','category':'Category',
                  'author':'Author','image':'Image'}
        
        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control','id':'title_id'}),
            'slug':forms.TextInput(attrs={'class':'form-control','id':'slug_id'}),
            'category':forms.Select(attrs={'class':'form-control','id':'category_id'}),
            'author':forms.Select(attrs={'class':'form-control','id':'author_id'})
        }