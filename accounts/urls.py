from django.urls import path, re_path
from . import views

urlpatterns = [
    path('new', views.signup, name='signup'), 
    path('verify/<slug:uidb64>/<slug:token>/', views.verify_account, name='verify'),
    path('', views.profile_view, name="myprofile"), 
    path('update', views.update_profile_view, name="update_profile"), 
    path('avatar', views.update_avatar_view, name="change_avatar"), 
    path('subscribe', views.subscribe_view, name="subscribe"), 
    path('unsubscribe', views.unsubscribe_view, name="unsubscribe"), 
    path('verification', views.verfiy_account_view, name="verify_account"), 
    path('myposts', views.myposts_view, name='myposts'), 
    path('mydrafts', views.mydrafts_view, name='mydrafts'), 
    path('mycomments', views.mycomments_view, name='mycomments'), 
    path('myfollowers', views.myfollowers_view, name='myfollowers'), 
    path('myfollowings', views.myfollowings_view, name='myfollowings'), 
    path('mytraffic', views.mytraffic_view, name='mytraffic'), 
    path('mysetting', views.mysetting_view, name='mysetting'), 
]