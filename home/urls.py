from django.urls import path
from . import views

urlpatterns = [
    path('', views.homeview, name='home'), 
    path('author/', views.author_list_view, name='author-list'), 
    path('author/<int:pk>/', views.author_detail_view, name='author-detail'), 
    path('subscribe/', views.add_to_sublist_view, name="add-to-sublist"), 
    path('TOS', views.terms_of_service_view, name="terms-of-service"), 
    path('feedback', views.feedback_view, name="feedback"), 
]


