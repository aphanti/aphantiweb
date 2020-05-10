from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.add_to_sublist_view, name="add-to-sublist"), 
]