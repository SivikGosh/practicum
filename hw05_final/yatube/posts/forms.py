""" формы приложения posts """

from django import forms

from .models import Comment, Post


class PostForm(forms.ModelForm):
    """ форма поста """
    class Meta:
        model = Post
        fields = ('text', 'group', 'image')

    def clean_text(self):
        text = self.cleaned_data['text']

        if len(text) == 0:
            raise forms.ValidationError('Поле текста пустое.')
        return text


class CommentForm(forms.ModelForm):
    """ форма комментария """
    class Meta:
        model = Comment
        fields = ['text']
