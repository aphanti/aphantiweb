from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from .models import Blog, Tag, Category, Comment
import markdown
from django.core.paginator import Paginator
from django.http import HttpResponse
from datetime import datetime
from .forms import BlogForm


blog_per_page = 10


def bloglistview(request):
    blog_list = Blog.objects.filter(is_draft=False).order_by('-publish_time')
    paginator = Paginator(blog_list,  blog_per_page)
    page = request.GET.get('page')
    blogs = paginator.get_page(page)
    return render(request, 'bloglist.html', {'blogs': blogs, 'num': len(blog_list)})


def blogdetailview(request, pk):
    blog = get_object_or_404(Blog, id = int(pk))
    blog.body = markdown.markdown(
        blog.body,
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.toc',
            'markdown.extensions.codehilite',
        ]
    )
    return render(request, 'blogdetail.html', {'blog': blog, 'comments':blog.comments.all().order_by('-create_time'), 'num_comment':len(blog.comments.all())})


def create_blog_view(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = BlogForm(request.POST)
            if form.is_valid():
                blog = form.save(commit=False)
                blog.author = request.user
                if 'save_to_draft' in request.POST:
                    blog.update_time = datetime.now()
                    blog.is_draft = True
                else:
                    blog.pub_time = datetime.now()
                    blog.is_draft = False

                blog.save()
                if blog.is_draft:
                    return redirect("mydrafts")
                else:
                    return redirect("myposts")
        else:
            form = BlogForm()
        return render(request, "create_blog.html", {"form": form})
    else:
        return redirect('login')


def update_blog_view(request, pk):
    if request.user.is_authenticated:
        instance = get_object_or_404(Blog, id=int(pk))

        if request.user.id == instance.author.id:
            if request.method == "POST":
                form = BlogForm(request.POST, instance=instance)
                if form.is_valid():
                    blog = form.save(commit = True)
                    if 'save_to_draft' in request.POST:
                        blog.update_time = datetime.now()
                        blog.is_draft = True
                    else:
                        blog.publish_time = datetime.now()
                        blog.is_draft = False
                    blog.save()
                    if blog.is_draft:
                        return redirect("mydrafts")
                    else:
                        return redirect("myposts")

            return render(request, "update_blog.html", {"form": BlogForm(instance=instance)})
        else:
            return redirect('blog-detail', pk=pk)
    else:
        return redirect('login')



