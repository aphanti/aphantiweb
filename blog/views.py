from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from .models import Blog, Tag, Category, Comment, Follow, BlogSearchTrack
import markdown
from django.core.paginator import Paginator
from django.http import HttpResponse
from datetime import datetime, timedelta
from .forms import BlogForm, CommentForm
from tracking_analyzer.models import Tracker
from django.utils import timezone
from django.http import Http404  
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
import random 
import os
import json 


blog_per_page = 10


def searching_blogs(text, blogs):
    text = text.lower()
    blogs = blogs.filter(title__icontains=text) | blogs.filter(author__display_name__icontains=text) | blogs.filter(tag__name__icontains=text) | blogs.filter(summary__icontains=text)
    return blogs.distinct()


def bloglistview(request):
    # get, no page:     all refresh
    # get, page:        check -> filter, content
    # post, no page:    filter, content
    # post, page:       filter, contant

    allcategory = ['All'] + [c.name for c in Category.objects.all()]
    allpasts = {'1 day':1, '1 week':7, '1 month':30, '6 months':180, '1 year':365, 'All time':9999}

    cats = [{'name':'All', 'selected': True}] + [{'name':c.name, 'selected':False} for c in Category.objects.all()]
    pasts = [{'value': x, 'checked': False} for x in allpasts]
    pasts[-1]['checked'] = True
    search_text = ''
    blog_list = Blog.objects.filter(is_draft=False)
    filtering = False

    if request.method == 'GET':
        if 'sortby' in request.GET:
            request.session['sortby'] = request.GET['sortby']
        if (('page' in request.GET) or ('sortby' in request.GET)) and ('blog_filter' in request.session):
            cats = request.session['blog_filter']['category']
            pasts = request.session['blog_filter']['past_time']
            search_text = request.session['blog_filter']['search_blog_text']
            filtering = True
        if 'category' in request.GET:
            cats = [{'name':x, 'selected':True} if x==request.GET['category'] else {'name':x, 'selected':False} for x in allcategory]
            filtering = True
        if 'search' in request.GET:
            search_text = request.GET['search']
            filtering = True
        if ('page' not in request.GET) and ('sortby' not in request.GET) and ('blog_filter' in request.session):
            request.session.pop('blog_filter')
    else:
        request.session['sortby'] = 'publish_time'
        filtering = True
        if 'category' in request.POST:
            cats = [{'name':x, 'selected':True} if x==request.POST['category'] else {'name':x, 'selected':False} for x in allcategory]
        if 'past_time' in request.POST:
            pasts = [{'value':x, 'checked':True} if x==request.POST['past_time'] else {'value':x, 'checked':False} for x in allpasts]
        if 'search_blog_text' in request.POST:
            search_text = request.POST['search_blog_text']

    if filtering:
        request.session['blog_filter'] = {'category':cats, 'past_time':pasts, 
            'search_blog_text': search_text}
        # filter by category
        tmp = [x['name'] for x in cats if x['selected']]
        if tmp[0] != 'All': blog_list = blog_list.filter(category__name=tmp[0])
        blogsearch = BlogSearchTrack(category=tmp[0])

        # filter by publish time
        tmp = [x['value'] for x in pasts if x['checked']]
        blog_list = blog_list.filter(publish_time__gte=timezone.now()-timedelta(days=allpasts[tmp[0]]))
        blogsearch.past_time = tmp[0]

        # search text
        if len(search_text) > 0:
            blogsearch.search_text = search_text
            blog_list = searching_blogs(search_text, blog_list)
        blogsearch.save()

    sortby = request.session.get('sortby', 'publish_time')
    if sortby == 'publish_time':
        blog_list = blog_list.order_by('-publish_time')
    if sortby == 'views':
        blog_list = blog_list.order_by('-num_visit')
    if sortby == 'likes':
        blog_list = blog_list.order_by('-num_like')
    if sortby == 'comments':
        blog_list = sorted(blog_list, key= lambda x: -(x.get_comment_count()))

    paginator = Paginator(blog_list,  blog_per_page)
    page = request.GET.get('page')
    blogs = paginator.get_page(page)


    return render(request, 'bloglist.html', \
        {'blogs': blogs, 'num': len(blog_list), 
        'category': cats, 
        'past_time': pasts, 
        'search_text': search_text, 
        'sortby': sortby })


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
                # comment = Comment(commenter=request.user, 
                #     content=request.POST['comment'], 
                #     blog=blog, 
                #     create_time = timezone.now() )
                # comment.save()
                comment_form = CommentForm(request.POST)
                if comment_form.is_valid():
                    comment = comment_form.save(commit=False)
                    comment.commenter = request.user 
                    comment.create_time = timezone.now()
                    comment.blog = blog
                    comment = comment_form.save(commit=True)
                    send_notify_comment_email(request, blog)
            
            if 'add_follow' in request.POST:
                add_follow(request, request.user, blog.author)
            
            if 'delete_follow' in request.POST:
                delete_follow(request.user.id, blog.author.id)

            if 'like_blog' in request.POST:
                if 'has_liked' not in request.session:
                    request.session['has_liked'] = [blog.id]
                    blog.num_like += 1
                    blog.save()
                    send_notify_like_email(request, blog)
                else:
                    if blog.id not in request.session['has_liked']:
                        tmp = request.session['has_liked']
                        tmp.append(blog.id) 
                        request.session['has_liked'] = tmp
                        blog.num_like += 1
                        blog.save()
                        send_notify_like_email(request, blog)
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
        comment_form = CommentForm()

        return render(request, 'blogdetail.html', {'blog': blog, 'comments':blog.comments.all().order_by('-create_time'), 'num_comment':len(blog.comments.all()), 'liked': liked, 
        'comment_form': comment_form})
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
                blog = form.save(commit=True)
                if 'save_to_draft' in request.POST:
                    blog.update_time = timezone.now()
                    blog.is_draft = True
                else:
                    blog.publish_time = timezone.now()
                    blog.is_draft = False
                blog.save()

                all_tag = [t.name for t in Tag.objects.all()]
                for name in request.POST:
                    if ('newtag_' in name):
                        if (request.POST[name] not in all_tag):
                            newtag = Tag(name=request.POST[name], bg_color=get_random_tag_color())
                            newtag.save()
                        else:
                            newtag = Tag.objects.get(name=request.POST[name])
                        blog.tag.add(newtag)
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

        update_flag = False
        if request.user.id == instance.author.id: 
            update_flag = True

        #-----------------------------------------------------
        # special access to certain blogs by certain users
        if not update_flag:
            update_blog_permission = dict()
            fjson = '/opt/aphanti/blog_update_permission.json'
            if os.path.exists(fjson):
                update_blog_permission = json.load(open(fjson, 'r'))
            if str(instance.id) in update_blog_permission:
                if request.user.id in update_blog_permission[str(instance.id)]:
                    update_flag = True
        #-----------------------------------------------------

        if update_flag:
            if request.method == "POST":
                form = BlogForm(request.POST, instance=instance)
                if form.is_valid():
                    blog = form.save(commit = True)
                    if 'save_to_draft' in request.POST:
                        blog.update_time = timezone.now()
                        blog.is_draft = True
                    else:
                        if blog.is_draft:
                            blog.publish_time = timezone.now()
                            blog.is_draft = False
                        else:
                            blog.update_time = timezone.now()
                    blog.save()

                    all_tag = [t.name for t in Tag.objects.all()]
                    for name in request.POST:
                        if ('newtag_' in name):
                            if (request.POST[name] not in all_tag):
                                newtag = Tag(name=request.POST[name], bg_color=get_random_tag_color())
                                newtag.save()
                            else:
                                newtag = Tag.objects.get(name=request.POST[name])
                            blog.tag.add(newtag)
                    blog.save()

                    if blog.is_draft:
                        return redirect("mydrafts")
                    else:
                        return redirect("myposts")

            return render(request, "update_blog.html", {"form": BlogForm(instance=instance), 'is_draft':instance.is_draft})
        else:
            return redirect('/blog/'+format(pk))
    else:
        return redirect('login')


def add_follow(request, follower, befollowed):
    follow = Follow(follower_id=follower.id, 
        befollowed_id=befollowed.id, 
        create_time = timezone.now())
    follow.save()
    send_notify_follow_email(request, follower, befollowed)
    return 

def delete_follow(follower_id, befollowed_id):
    follow = Follow.objects.filter(follower_id=follower_id).filter(befollowed_id=befollowed_id)
    if follow:
        follow.delete()
    return 


def get_random_tag_color():
    rgb = random.choices(range(128,256), k=3)
    return "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])


def send_notify_comment_email(request, blog):
    if blog.author.setting_notify_comment:
        subject = "New comment on your blog"
        message = render_to_string('notify_comment_email.html', {
            'blog': blog, 
            'domain': get_current_site(request).domain, 
            })
        blog.author.email_user(subject=subject, message=message)
    return 

def send_notify_like_email(request, blog):
    if blog.author.setting_notify_like:
        subject = "New like on your blog"
        message = render_to_string('notify_like_email.html', {
            'blog': blog, 
            'domain': get_current_site(request).domain, 
            })
        blog.author.email_user(subject=subject, message=message)
    return 


def send_notify_follow_email(request, follower, befollowed):
    if befollowed.setting_notify_follow:
        subject = "New follower on www.aphanti.com"
        message = render_to_string('notify_follow_email.html', {
            'follower': follower, 
            'domain': get_current_site(request).domain, 
            })
        befollowed.email_user(subject=subject, message=message)
    return 

