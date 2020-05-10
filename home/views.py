from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404

from accounts.models import WebUser


def homeview(request):
    return render(request, 'home.html', context = {})
    

def author_list_view(request):
    authors = WebUser.objects.filter(is_verified=True)
    return render(request, 'author_list.html', context = {'authors': authors, 'num': len(authors)})


def author_detail_view(request, pk):
    author = get_object_or_404(WebUser, id=int(pk))
    return render(request, 'author_detail.html', context={'author': author})



