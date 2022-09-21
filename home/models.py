from django.db import models

# Create your models here.

from django.utils.translation import ugettext_lazy
from ckeditor.fields import RichTextField


class SubscribeList(models.Model):
    email = models.EmailField(ugettext_lazy('email address'), unique=True)
    def __str__(self):
        return self.email 

    class Meta:
        ordering = ['email']
        verbose_name = "Subscribe List"


class Feedback(models.Model):
    email = models.EmailField(ugettext_lazy('email address'))
    body = RichTextField(config_name='feedback')
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta: 
        ordering = ['-create_time']
        
