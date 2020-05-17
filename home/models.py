from django.db import models

# Create your models here.

from django.utils.translation import ugettext_lazy


class SubscribeList(models.Model):
    email = models.EmailField(ugettext_lazy('email address'), unique=True)
    def __str__(self):
        return self.email 

    class Meta:
        ordering = ['email']
        verbose_name = "Subscribe List"
