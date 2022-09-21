from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404

from aphantiweb.settings import web_info
from accounts.models import WebUser
from blog.models import Category, Tag
from blog.views import add_follow, delete_follow
from .models import SubscribeList
from .forms import FeedbackForm

from django.http import Http404  
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site

from datetime import datetime
from django.http import JsonResponse


from django.views.decorators.csrf import csrf_exempt
import os
import json 


@csrf_exempt
def bible_ecclesiastes(request):
    return render(request, "bible_ecclesiastes.html")

@csrf_exempt
def PA1cam(request):
    if request.method == 'POST':
        if 'password' in request.POST:
            if request.POST['password'] == web_info["esp32cam_password_PA1"]:
                return render(request, 'PA1cam_stream.html')
    
    return render(request, 'PA1cam_login.html') 


@csrf_exempt
def MAcam(request):
    if request.method == 'POST':
        if 'password' in request.POST:
            if request.POST['password'] == web_info["esp32cam_password_MA"]:
                return render(request, 'MAcam_stream.html')
    
    return render(request, 'MAcam_login.html') 


@csrf_exempt
def esp32cam_settings(request):
    fsave = web_info["esp32cam_settings_json"]
    #if request.method == 'POST':
    #    if 'IP' in request.POST:
    #        obj = {'IP': request.POST['IP'], 'datetime':datetime.now().isoformat()}
    #        json.dump(obj, open(fsave, 'w'), indent=4)
    try:
        obj = json.load(open(fsave, 'r'))
    except:
        obj = {}
    return JsonResponse(obj)
    

def testapi_get(request):
    data = {'test_message': "hi there, welcome to aphanti.com!", 'test_time': datetime.now().isoformat()}
    return JsonResponse(data)


# ========================================================================
# aphanti web views

def homeview(request):
    return render(request, 'home.html', 
        context = {'categories': Category.objects.all().distinct() , 
        'tags': Tag.objects.all().distinct() })
    

def author_list_view(request):
    authors = WebUser.objects.filter(is_verified=True).filter(is_author=True).distinct()
    return render(request, 'author_list.html', context = {'authors': authors, 'num': len(authors)})


def author_detail_view(request, pk):
    author = get_object_or_404(WebUser, id=int(pk))
    #if author.is_verified and author.is_author:
    if request.method == 'POST':
        if 'add_follow' in request.POST:
            add_follow(request, request.user, author)
            #send_notify_follow_email(request, request.user, author)
        
        if 'delete_follow' in request.POST:
            delete_follow(request.user.id, author.id)

    return render(request, 'author_detail.html', context={'author': author})
    #else:
    #    raise Http404  

def add_to_sublist_view(request):
    if request.method == 'POST':
        if not SubscribeList.objects.filter(email = request.POST['email']).exists():
            obj = SubscribeList.objects.create(email = request.POST['email'])

        return render(request, 'add_sublist_done.html', {'email': request.POST['email']})
    else:
        return redirect('home')

def terms_of_service_view(request):
    return render(request, 'terms_of_service.html', {})
    

def feedback_view(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return render(request, "feedback_done.html", {"email": request.POST['email']})
    else:
        form = FeedbackForm()
    return render(request, "feedback.html", {"form": form})



