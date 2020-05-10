from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [ 
    path('', views.bloglistview, name="blog-list"), 
    path('create/', views.create_blog_view, name="create-blog"), 
    path('<int:pk>/', views.blogdetailview, name='blog-detail'), 
    path('<int:pk>/update/', views.update_blog_view, name="update-blog"), 
]

