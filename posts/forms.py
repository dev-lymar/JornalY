from django import forms
from .models import Post, Group


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'group']
        widgets = {
            'group': forms.Select(attrs={'class': 'form-control'})
        }

    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=False, empty_label='---------')
