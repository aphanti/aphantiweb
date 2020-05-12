from django.shortcuts import render

# Create your views here.

from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm
from .models import WebUser
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .token import account_activation_token
from django.core.paginator import Paginator

from blog.models import Blog, Comment, Follow

post_per_page = 6
comment_per_page = 10


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.set_password(form.cleaned_data['password'])
            user.save()

            # get current site
            current_site = get_current_site(request)
            subject = "Welcome to www.aphanti.com"
            # create Message
            message = render_to_string('account_verify_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            # send verification link to the user
            user.email_user(subject=subject, message=message)

            user = authenticate(email=user.email, password=form.cleaned_data['password'])
            login(request, user)
            return render(request, 'signup_done.html', {'email': user.email})            
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def verify_account(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = WebUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, WebUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_verified = True
        user.save()
        login(request, user)
        return render(request, 'account_verify_done.html', {'email': user.email})
    else:
        return render(request, 'account_verify_invalid.html')


def profile_view(request):
    if request.user.is_authenticated:
        return render(request, 'myprofile.html', {'user': request.user})
    else:
        return redirect('login')


def update_profile_view(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            request.user.display_name = request.POST['display_name']
            request.user.first_name = request.POST['first_name']
            request.user.last_name = request.POST['last_name']
            request.user.bio = request.POST['bio']
            request.user.save()

        return render(request, 'myprofile.html', {'user': request.user})
    else:
        return redirect('login')


def update_avatar_view(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            request.user.avatar.save( str(request.user.id)+'.avatar', request.FILES['avatar'])
            request.user.save()

        return render(request, 'myprofile.html', {'user': request.user})
    else:
        return redirect('login')


def subscribe_view(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            request.user.is_subscribe = True
            request.user.save()
            
        return render(request, 'myprofile.html', {'user': request.user})
    else:
        return redirect('login')


def unsubscribe_view(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            request.user.is_subscribe = False 
            request.user.save()
            
        return render(request, 'myprofile.html', {'user': request.user})
    else:
        return redirect('login')


def verfiy_account_view(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            # get current site
            current_site = get_current_site(request)
            subject = "Welcome to www.aphanti.com"
            # create Message
            message = render_to_string('verification.html', {
                'user': request.user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(request.user.pk)),
                'token': account_activation_token.make_token(request.user),
            })
            # send activation link to the user
            request.user.email_user(subject=subject, message=message)
            
        return render(request, 'myprofile.html', {'user': request.user})
    else:
        return redirect('login')


def myposts_view(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            blog = get_object_or_404(Blog, id=int(request.POST['delete_blog_id']))
            blog.delete()
            
        blog_list = request.user.get_myposts()
        paginator = Paginator(blog_list, post_per_page)
        page = request.GET.get('page')
        blogs = paginator.get_page(page)        
        return render(request, 'myposts.html', {'blogs': blogs, 'num': len(blogs)})
    else:
        return redirect('login')


def mydrafts_view(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            blog = get_object_or_404(Blog, id=int(request.POST['delete_blog_id']))
            blog.delete()
            
        blog_list = request.user.get_mydrafts()
        paginator = Paginator(blog_list, post_per_page)
        page = request.GET.get('page')
        blogs = paginator.get_page(page)        
        return render(request, 'mydrafts.html', {'blogs': blogs, 'num': len(blogs)})
    else:
        return redirect('login')    


def mycomments_view(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pass 
            
        clist = request.user.get_mycomments()
        paginator = Paginator(clist, comment_per_page)
        page = request.GET.get('page')
        comments = paginator.get_page(page)        
        return render(request, 'mycomments.html', {'comments': comments, 'num': len(comments)})
    else:
        return redirect('login')    


def myfollowers_view(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pass
            
        people = request.user.get_myfollowers()
        return render(request, 'myfollowers.html', {'people': people, 'num': len(people)})
    else:
        return redirect('login')    


def myfollowings_view(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pass
            
        people = request.user.get_myfollowings()
        return render(request, 'myfollowings.html', {'people': people, 'num': len(people)})
    else:
        return redirect('login')    

