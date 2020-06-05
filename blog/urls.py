from django.urls import path
from . import views
from ckeditor_uploader import views as uploader_views

app_name = 'blog'

urlpatterns = [ 
    path('', views.bloglistview, name="blog-list"), 
    path('create/', views.create_blog_view, name="create-blog"), 
    path('<int:pk>/', views.blogdetailview, name='blog-detail'), 
    path('<int:pk>/update/', views.update_blog_view, name="update-blog"), 
    path('ckeditor/upload/', 
        uploader_views.upload, name='ckeditor_upload'), 
    path('ckeditor/browse/', 
        uploader_views.browse, name='ckeditor_browse'), 
]

