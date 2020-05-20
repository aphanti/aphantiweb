from django.contrib import admin

# Register your models here.
from .models import SubscribeList, Feedback


@admin.register(SubscribeList)
class SubscribeListAdmin(admin.ModelAdmin):
    list_display = ('email', )
    fields = ['email', ]
    #list_filter = ['email', ]


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('create_time', 'email')
    fields = ['email', 'body']
    list_filter = ['email']
    readonly_fields = ['create_time']

