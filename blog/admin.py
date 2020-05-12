from django.contrib import admin

# Register your models here.

from .models import Blog, Comment, Tag, Category, Follow
from django.utils.html import format_html
from django.utils.safestring import mark_safe

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'create_time', 'is_draft']
    fields = ['title', ('author', 'create_time', 'update_time', 'publish_time'), 
        'is_draft', 'category', 'tag', 'summary', 'body']
    list_filter = ( 'author', 'category', 'tag', 'is_draft' )
    #readonly_fields = ('pub_time', )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'bg_color')
    fields = ('name', 'bg_color')
    #list_filter = ('name', 'bg_color')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'bg_image')
    fields = ('name', 'bg_image')
    #list_filter = ('name', 'bg_image')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('create_time', 'author', 'blog')
    fields = [('create_time', 'author'), 'blog', 'content']
    list_filter = ['author', 'blog']


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'befollowed', 'create_time')
    fields = ['follower', 'befollowed', 'create_time']
    #list_filter = ['follower', 'befollowed']

