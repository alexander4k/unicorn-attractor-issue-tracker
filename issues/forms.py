from django import forms
from django.forms import ModelForm
from .models import Issue, Comment

class IssueForm(ModelForm):
    class Meta:
        model = Issue
        fields = ['title', 'issue_type', 'description']
        
class CommentForm(ModelForm):
    content = forms.CharField(label="Enter your comment:", widget=forms.Textarea(attrs={'rows': 3}))
    class Meta:
        model = Comment
        fields = ['content']