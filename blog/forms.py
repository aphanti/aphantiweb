from django import forms
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Blog, Comment, Tag, Category


class BlogForm(forms.ModelForm):
    body = forms.CharField(widget = CKEditorUploadingWidget(), required=True)
    class Meta:
        model = Blog
        fields = ('title', 'summary', 'category', 'tag', 'body')


class DeleteNewForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = []
