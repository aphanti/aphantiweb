from django.db import models

# Create your models here.

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
from datetime import datetime


class Blog(models.Model):
    author = models.ForeignKey('accounts.WebUser', on_delete=models.CASCADE, 
        null=False, blank=False)
    title = models.CharField(max_length=400)
    summary = models.TextField(max_length=4000, blank=True)
    body = RichTextUploadingField()
    create_time = models.DateTimeField(default=datetime.now())
    update_time = models.DateTimeField(default=datetime.now())
    publish_time = models.DateTimeField(default=datetime.now())
    category = models.ForeignKey('Category', on_delete=models.CASCADE, \
        verbose_name="Blog category")
    tag = models.ManyToManyField('Tag', verbose_name='Blog Tag', blank=True)
    is_draft = models.BooleanField(default=True, verbose_name='Is draft')

    def __str__(self):
        return self.title + ' - ' + self.author.display_name

    def get_absolute_url(self):
        return reverse('blog:blog-detail', args=[str(self.id)])


class Tag(models.Model):
    name = models.CharField(max_length=128, blank=False, unique=True)
    def __str__(self):
        return self.name

    def get_blog_count(self):
        return Blog.objects.filter(tag__name=self.name).distinct().count()

    class Meta:
        ordering = ['name']
        verbose_name = "Tag"


class Category(models.Model):
    name = models.CharField(max_length=128, blank=False, unique=True)
    def __str__(self):
        return self.name

    def get_blog_count(self):
        return Blog.objects.filter(category__name=self.name).distinct().count()

    class Meta:
        ordering = ['name']
        verbose_name = "Category"


class Comment(models.Model):
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE, null=True, related_name='comments')
    author = models.ForeignKey('accounts.WebUser', on_delete=models.CASCADE, null=False)
    content = models.TextField(max_length=4000, blank=True)
    create_time = models.DateTimeField(blank=True)

    def __str__(self):
        return "[" + self.create_time.strftime("%m/%d/%Y, %H:%M:%S")+ "] " + self.author.display_name + "'s comment on " + self.blog.title

    class Meta:
        ordering = ['create_time']


class Follow(models.Model):
    befollowed = models.ForeignKey('accounts.WebUser', on_delete=models.CASCADE, blank=True, 
        related_name='befollowed')
    follower = models.ForeignKey('accounts.WebUser', on_delete=models.CASCADE, blank=True, 
        related_name='follower')

    def __str__(self):
        return self.follower.display_name + '->' + self.befollowed.display_name

    class Meta:
        ordering = ['follower']

