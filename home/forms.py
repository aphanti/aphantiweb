from django import forms
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Feedback


class FeedbackForm(forms.ModelForm):
    body = forms.CharField(widget = CKEditorWidget(config_name='feedback'), required=True)
    class Meta:
        model = Feedback
        fields = ('email', 'body' )