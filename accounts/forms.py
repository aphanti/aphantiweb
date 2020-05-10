from django import forms
#from django.contrib.auth.forms import UserCreationForm
from .models import WebUser

class SignUpForm(forms.ModelForm):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = WebUser
        fields = ('email', 'password')


