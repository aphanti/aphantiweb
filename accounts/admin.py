from django.contrib import admin

# Register your models here.

from django.contrib.auth.admin import UserAdmin

from .models import WebUser
from django.utils.translation import ugettext_lazy
from django.utils.html import format_html
from django.utils.safestring import mark_safe


@admin.register(WebUser)
class WebUserAdmin(UserAdmin):
    list_display = ('email', 'display_name', 'is_active', 'is_staff', 'is_superuser', 
        'is_verified', 'is_subscribe', 'is_author', 'show_photo')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 
        'is_verified', 'is_subscribe', 'is_author')

    fieldsets = ( 
        (None, {'fields': ('email', 'password')}),
        (ugettext_lazy('Personal info'), {'fields': (('display_name', 'first_name', 'last_name'), ( 'is_verified', 'is_subscribe', 'is_author'), ('setting_show_email', 'setting_show_fullname', 'setting_notify_comment', 'setting_notify_like', 'setting_notify_follow', 'setting_notify_new_blog'), 'avatar', 'bio')}),
        (ugettext_lazy('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (ugettext_lazy('Important dates'), {'fields': ('last_login', 'date_joined')}),
        )

    ordering = ('email',)
    search_fields = ('display_name', 'first_name', 'last_name', 'email')

    def show_photo(self, obj):
        return mark_safe('<img src="{url}" width="70px" height="70px" />'.format(url = obj.avatar.url))




