from django import forms
from .models import Comment , Post



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("name", 'email' ,'site' , 'comment')

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title' , 'short_description' , 'description' , 'image']