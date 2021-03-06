from django import forms
from .models import Topic,Post


class NewTopicForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea(attrs={'rows':5,'placeholder':'Whats in your mind'}),
                              max_length=4000,
                              help_text='Max Length is 4000'
                              )

    class Meta:
        model = Topic
        fields = ['subject', 'message']


class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message']
