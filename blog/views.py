from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from .models import Blog, Tag, Category, Comment, Follow
import markdown
from django.core.paginator import Paginator
from django.http import HttpResponse
from datetime import datetime
from .forms import BlogForm
from tracking_analyzer.models import Tracker
from django.utils import timezone
from django.http import Http404  
from django.http import HttpResponseRedirect



blog_per_page = 10


def bloglistview(request):
    blog_list = Blog.objects.filter(is_draft=False).order_by('-publish_time')
    paginator = Paginator(blog_list,  blog_per_page)
    page = request.GET.get('page')
    blogs = paginator.get_page(page)
    return render(request, 'bloglist.html', {'blogs': blogs, 'num': len(blog_list)})


def blogdetailview(request, pk):
    blog = get_object_or_404(Blog, id = int(pk))
    if (not blog.is_draft) or (request.user.is_authenticated and (request.user.id == blog.author.id)):
        blog.body = markdown.markdown(
            blog.body,
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.toc',
                'markdown.extensions.codehilite',
            ]
        )

        if request.method=='POST':
            if 'publish_comment' in request.POST:
                comment = Comment(commenter=request.user, 
                    content=request.POST['comment'], 
                    blog=blog, 
                    create_time = timezone.now() )
                comment.save()
            
            if 'add_follow' in request.POST:
                add_follow(request.user.id, blog.author.id)
            
            if 'delete_follow' in request.POST:
                delete_follow(request.user.id, blog.author.id)

            if 'like_blog' in request.POST:
                if 'has_liked' not in request.session:
                    request.session['has_liked'] = [blog.id]
                    blog.num_like += 1
                    blog.save()
                else:
                    if blog.id not in request.session['has_liked']:
                        tmp = request.session['has_liked']
                        tmp.append(blog.id) 
                        request.session['has_liked'] = tmp
                        blog.num_like += 1
                        blog.save()
                    else:
                        tmp = list(set(request.session['has_liked']))
                        tmp.remove(blog.id) 
                        request.session['has_liked'] = tmp
                        blog.num_like -= 1
                        blog.save()


        if 'has_viewed' not in request.session:
            request.session['has_viewed'] = [blog.id]
            blog.num_visit += 1
            blog.save()
        else:
            if blog.id not in request.session['has_viewed']:
                tmp = request.session['has_viewed']
                tmp.append(blog.id) 
                request.session['has_viewed'] = tmp
                blog.num_visit += 1
                blog.save()

        if ('has_liked' in request.session) and (blog.id in request.session['has_liked']):
            liked = True        
        else:
            liked = False

        Tracker.objects.create_from_request(request, blog)

        return render(request, 'blogdetail.html', {'blog': blog, 'comments':blog.comments.all().order_by('-create_time'), 'num_comment':len(blog.comments.all()), 'liked': liked})
    else:
        if not request.user.is_authenticated:
            return HttpResponseRedirect("/accounts/login/?next=/blog/"+format(pk))
        else:
            raise Http404


def create_blog_view(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = BlogForm(request.POST)
            if form.is_valid():
                blog = form.save(commit=False)
                blog.author = request.user                
                if 'save_to_draft' in request.POST:
                    blog.update_time = timezone.now()
                    blog.is_draft = True
                else:
                    blog.publish_time = timezone.now()
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
                        blog.update_time = timezone.now()
                        blog.is_draft = True
                    else:
                        blog.publish_time = timezone.now()
                        blog.is_draft = False
                    blog.save()
                    if blog.is_draft:
                        return redirect("mydrafts")
                    else:
                        return redirect("myposts")

            return render(request, "update_blog.html", {"form": BlogForm(instance=instance), 'is_draft':instance.is_draft})
        else:
            return redirect('blog-detail', pk=pk)
    else:
        return redirect('login')


def add_follow(follower_id, befollowed_id):
    follow = Follow(follower_id=follower_id, 
        befollowed_id=befollowed_id, 
        create_time = timezone.now())
    follow.save()
    return 

def delete_follow(follower_id, befollowed_id):
    follow = Follow.objects.filter(follower_id=follower_id).filter(befollowed_id=befollowed_id)
    if follow:
        follow.delete()
    return 
