from django.contrib import admin

# Register your models here.

from .models import SubscribeList


@admin.register(SubscribeList)
class SubscribeListAdmin(admin.ModelAdmin):
    list_display = ('email', )
    fields = ['email', ]
    list_filter = ['email', ]


