from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404

from accounts.models import WebUser
from blog.models import Category, Tag
from blog.views import add_follow, delete_follow
from .models import SubscribeList
from .forms import FeedbackForm
from django.http import Http404  
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site



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



