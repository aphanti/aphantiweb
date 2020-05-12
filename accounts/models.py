from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser, AbstractBaseUser

from django.utils.translation import ugettext_lazy
from .managers import UserManager

from blog.models import Blog, Comment, Follow


class WebUser(AbstractUser):
    #username = models.CharField(primary_key=False, max_length=128, unique=False, \
    #    verbose_name='username', blank=True)
    username = None
    email = models.EmailField(ugettext_lazy('email address'), unique=True)
    display_name = models.CharField(max_length=128, default='anonymous')
    avatar = models.ImageField(upload_to="user_avatar/", blank=True, 
        default='user_avatar/default.jpg', verbose_name='Profile photo')
    bio = models.TextField(max_length=1000, blank=True, verbose_name='Self-description')

    is_verified = models.BooleanField(default=False, verbose_name='is verified')
    is_subscribe = models.BooleanField(default=True, verbose_name='is subscribe')

    USERNAME_FIELD = 'email'
    #REQUIRED_FIELDS = ['email']
    REQUIRED_FIELDS = []


    objects = UserManager()

    def __str__(self):
        return self.display_name

    def get_blog_count(self):
        return Blog.objects.filter(author__id=self.id).exclude(is_draft=True).distinct().count()

    def get_draft_count(self):
        return Blog.objects.filter(author__id=self.id).filter(is_draft=True).distinct().count()        

    def get_comment_count(self):
        return Comment.objects.filter(author__id=self.id).distinct().count()

    def get_myposts(self):
        return Blog.objects.filter(author__id=self.id).exclude(is_draft=True).order_by('-publish_time')

    def get_mydrafts(self):
        return Blog.objects.filter(author__id=self.id).filter(is_draft=True).order_by('-update_time')

    def get_mycomments(self):
        return Comment.objects.filter(author__id=self.id).order_by('-create_time')

    def get_follower_count(self):
        return Follow.objects.filter(befollowed__id=self.id).distinct().count()

    def get_myfollowers(self):
        fs = Follow.objects.filter(befollowed__id=self.id).distinct()
        people = []
        for f in fs:
            people.append( f.follower )
        return people

    
    def get_following_count(self):
        return Follow.objects.filter(follower__id=self.id).distinct().count()

    def get_myfollowings(self):
        fs = Follow.objects.filter(follower__id=self.id)
        people = []
        for f in fs:
            people.append( f.befollowed )
        return people

    def get_myfollowing_ids(self):
        fs = Follow.objects.filter(follower__id=self.id)
        ids = []
        for f in fs:
            ids.append( f.befollowed.id )
        return ids


