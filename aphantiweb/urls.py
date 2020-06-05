"""aphantiweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from ckeditor_uploader import views as uploader_views
from django.views.decorators.cache import never_cache


urlpatterns = [
    path('admin/', admin.site.urls), 
    path('ckeditor/', include('ckeditor_uploader.urls')), 
    path('', include('home.urls')), 
    path('blog/', include('blog.urls')), 
]

# Use static() to add url mapping to serve static files during development (only)
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#urlpatterns += [ path('ckeditor/', include('ckeditor_uploader.urls'), name='ckeditor'), 
#    path('ckeditor/upload/', uploader_views.upload, name='ckeditor_upload'), 
#    path('ckeditor/browse/', never_cache(uploader_views.browse), name='ckeditor_browse'),  ]

#Add Django site authentication urls (for login, logout, password management)
urlpatterns += [ 
    path('accounts/', include('django.contrib.auth.urls')),    
    path('accounts/', include('allauth.urls')), 
    path('accounts/', include('accounts.urls')), 
]