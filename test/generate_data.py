import os 
import sys 
import json 
import glob 
import copy 
import MySQLdb
import random
from datetime import datetime, timedelta
import django 
from django.core.files import File
from django.utils import timezone
import pytz

proj_dir = os.path.dirname(os.path.abspath(__file__)) + '/../'
sys.path.append( proj_dir )
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aphantiweb.settings')
django.setup()  

from aphantiweb.settings import WEB_INFO_JSON, SITE_ID
from accounts.models import WebUser
from allauth.socialaccount.models import SocialApp
from blog.models import Blog, Comment, Category, Tag, Follow
from home.models import SubscribeList
from django.contrib.sites.models import Site
from tracking_analyzer.models import Tracker
from django.contrib.gis.geoip2 import GeoIP2, GeoIP2Exception
from django.http import HttpRequest
from geoip2.errors import GeoIP2Error

resource_names = []
resource_words = []
resource_images = []



def get_resource(config):
    global resource_names, resource_words, resource_images
    print('get resources')
    resource_names = list(set([line.strip().lower() for line in open(config['user_name'], 'r').readlines() if len(line.strip())>0]))
    resource_words = [line.strip() for line in open(config['words'], 'r').readlines() if len(line.strip())>0]
    resource_images = glob.glob(config['random_image']+'/*')
    return 


def upload_default(config):
    os.system('mkdir -p '+proj_dir+'/uploads/user_avatar')
    os.system('mkdir -p '+proj_dir+'/uploads/blog_category')
    os.system('mkdir -p '+proj_dir+'/uploads/blog_body_image')
    os.system('cp -f resource/user_avatar_default.jpg '+proj_dir+'/uploads/user_avatar/default.jpg')
    os.system('cp -f resource/category_bg_default.png '+proj_dir+'/uploads/blog_category/default.png')


def get_database_connection(config):
    print('get database connected')
    web_info = json.load(open(WEB_INFO_JSON, 'r'))
    user = web_info['APHANTI_MYSQL_USER']
    host = "localhost"
    passwd = web_info['APHANTI_MYSQL_PASSWORD']
    dbname = web_info['APHANTI_MYSQL_DBNAME']
    return MySQLdb.connect(host=host, user=user, passwd=passwd, db=dbname)
    

def generate_users(config):
    print('--- delete all users ---')
    WebUser.objects.all().delete()
    
    ids = []
    
    print('create superuser:', config['superuser_email'])
    user = WebUser(email = config['superuser_email'])
    user.id = 9999
    user.set_password(config['user_password'])
    user.display_name = 'Administrator'
    user.is_active = True 
    user.is_staff = True
    user.is_superuser = True 
    user.is_verified = True
    user.is_author = False
    user.save() 

    names = random.sample(resource_names, config['num_user'])
    for i in range(len(names)):
        name = names[i]
        print('create non-staff user:', name)
        user = WebUser(email = name.lower()+'@example.com')
        user.id = i + 1
        user.set_password(config['user_password'])
        user.display_name = name
        user.first_name = random.choice(resource_names)
        user.last_name = random.choice(resource_names)
        if random.random() < config['user_verify_prob']:
            user.is_verified = True
            user.is_author = True

        if random.random() < 0.5:
            user.setting_show_email = True
        if random.random() < 0.5:
            user.setting_show_fullname = True
        
        if random.random() < config['user_has_avatar_prob']:
            fsource = random.choice(resource_images)
            fsave = format(user.id)+'.avatar'
            os.system('cp -f '+fsource+' '+proj_dir+'/uploads/user_avatar/'+fsave)
            user.avatar = 'user_avatar/'+fsave
        bio_length = random.choice(range(config['bio_length_range'][0], config['bio_length_range'][1]))
        if bio_length > 0:
            user.bio = ' '.join( random.choices(resource_words, k=bio_length) )
        user.save() 

        if user.is_verified and user.is_author:
            ids.append(user.id)

    return ids


def generate_category(config):
    print('--- delete all categories ---')
    Category.objects.all().delete()

    ids = []
    for i in range(config['num_category']):
        c = Category(name = random.choice(resource_words), id=i+1)
        print('create category:', c.name)
        fsource = random.choice(resource_images)
        fsave = 'blog_category/'+format(c.id)+'.category'
        os.system('cp -f '+fsource+' '+proj_dir+'/uploads/'+fsave)
        c.bg_image = fsave
        c.save()
        ids.append(c.id)

    return  ids


def rgb2hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])


def generate_tag(config):
    print('--- delete all tags ---')
    Tag.objects.all().delete()

    ids = []
    for i in range(config['num_tag']):
        c = Tag(name = random.choice(resource_words), id=i+1)
        c.bg_color = rgb2hex(random.choices(list(range(128,256)), k=3))
        print('create tag:', c.name, c.bg_color)
        c.save()
        ids.append(c.id)
    return  ids


def generate_blog(config, user_ids, category_ids, tag_ids):
    print('--- delete all blogs ---')
    Blog.objects.all().delete()

    time0 = timezone.now() - timedelta(days=abs(config['hist_day'][0]))
    dsecond = 86400*(abs(config['hist_day'][0] - config['hist_day'][1]))

    ids = []
    npic = 0
    for i in range(config['num_blog']):
        print('generate blog', i+1)
        create_time = time0 + timedelta(seconds = int(1.0*random.random()*dsecond))
        blog = Blog( id=i+1, author_id = random.choice(user_ids), 
            category_id = random.choice(category_ids), 
            is_draft = random.choice([True, False]), 
            create_time = create_time, 
            publish_time = create_time + timedelta(days = 1), 
            update_time = create_time + timedelta(days = 2) )
        blog.save()
        if not blog.is_draft:
            blog.num_visit = random.choice(range(config['blog_maxvisit']))
            blog.num_like = random.choice(range(config['blog_maxlike']))
        ntag = random.choice( range(config['blog_tag_range'][0], config['blog_tag_range'][1]) )
        if ntag > 0:
            for itag in random.sample( tag_ids, ntag ):
                blog.tag.add( Tag.objects.get(pk = itag) )
        blog.title = get_random_sentence(config['blog_title_length_range'])
        blog.summary = get_random_sentence(config['blog_summary_length_range'])
        num_para = random.choice(range(config['blog_body_paragraph_num_range'][0], 
            config['blog_body_paragraph_num_range'][1]))
        ipic = random.choice(range(num_para + 1))
        for k in range(num_para+1):
            if (k == ipic):
                if (random.random() < config['blog_body_has_image_prob']):
                    fsource = random.choice(resource_images)
                    fsave = "blog_body_image/"+format(npic+1)+'.blog'
                    os.system('cp -f '+fsource+' '+proj_dir+'/uploads/'+fsave)
                    blog.body += '<img width=100% src="/media/'+fsave+'"></img>'
                    npic += 1
            else:
                blog.body += "<p>"+ get_random_sentence(config['blog_body_paragraph_length_range']) +"</p>"
        blog.save()
    
        if not blog.is_draft:
            ids.append(blog.id)

    return ids 


def generate_comments(config, user_ids, blog_ids):
    print('--- delete all comments ---')
    Comment.objects.all().delete()

    time0 = timezone.now() - timedelta(days=abs(config['hist_day'][0]))
    dsecond = 86400*(abs(config['hist_day'][0] - config['hist_day'][1]))

    ids = []
    for i in range(config['num_comment']): 
        print('generate comment:', i+1)
        comment = Comment(id=i+1, blog_id = random.choice(blog_ids), 
            commenter_id = random.choice(user_ids), 
            content = get_random_sentence(config['comment_length_range']))
        comment.create_time = time0 + timedelta(seconds = int(1.0*random.random()*dsecond))
        comment.save()
        ids.append(comment.id)
    
    return ids 


def generate_follow(config, user_ids):
    print('--- delete all follows ---')
    Follow.objects.all().delete()

    time0 = timezone.now() - timedelta(days=abs(config['hist_day'][0]))
    dsecond = 86400*(abs(config['hist_day'][0] - config['hist_day'][1]))

    ids = []
    tmp = list(set([ tuple(random.sample(user_ids, 2)) for i in range(config['num_follow'])]))
    for i in range(len(tmp)):
        print('generate follow:', i+1)
        people = tmp[i]
        follow = Follow(id = i+1, follower_id = people[0], befollowed_id = people[1])
        follow.create_time = time0 + timedelta(seconds = int(1.0*random.random()*dsecond) )
        follow.save()
        ids.append(follow.id)
    return ids 


def get_random_sentence(length_range):
    length = random.choice(range(length_range[0], length_range[1]))
    if length > 0:
        return ' '.join(random.choices(resource_words, k=length))
    else:
        return ''


def generate_tracker(config, blog_ids):
    print('--- delete all tracker ---')
    Tracker.objects.all().delete()

    time0 = timezone.now() - timedelta(days=abs(config['hist_day'][0]))
    dsecond = 86400*(abs(config['hist_day'][0] - config['hist_day'][1]))
    ids = []
    for i in range(config['num_tracker']):

        blogid = random.choice(blog_ids)
        blog = Blog.objects.get(id=blogid)
        
        #request = HttpRequest(path='/blog/'+format(blogid), method='GET')
        #track = Tracker.objects.create_from_request(request, blog)

        city = {}
        # Get the IP address and so the geographical info, if available.
        ip_address = '.'.join([format(x) for x in random.choices(range(256), k=4)])
        print('generate tracker', i+1, ':', ip_address)

        geo = GeoIP2()
        try:
            city = geo.city(ip_address)
        except (GeoIP2Error, GeoIP2Exception):
            print('Unable to determine geolocation for address:', ip_address)

        track = Tracker.objects.create(
            id = i+1, 
            content_object=blog,
            ip_address=ip_address,
            ip_country=city.get('country_code', '') or '',
            ip_region=city.get('region', '') or '',
            ip_city=city.get('city', '') or '',
            device_type=random.choice(['pc', 'mobile', 'tablet', 'bot', 'unknown']), 
            device='test', 
            browser='test', 
            browser_version='0', 
            system='test', 
            system_version='0', 
            user=None, 
        )
        track.timestamp = time0 + timedelta(seconds = int(1.0*random.random()*dsecond) )
        track.save()
        ids.append(track.id)
    return ids


def setup_social_account(config):
    print('--- delete all sites and social app ---')
    Site.objects.all().delete()
    SocialApp.objects.all().delete()

    print('set up google app ')
    web_info = json.load(open(WEB_INFO_JSON, 'r'))
    site = Site(id=SITE_ID, domain=web_info['domain_name'], name=web_info['domain_name'])
    site.save()

    socialapp = SocialApp( id=1, \
        provider = 'google', 
        name = 'Google API', 
        client_id = web_info['google_app_client_id'], 
        secret = web_info['google_app_client_secret'], 
        key = web_info['google_app_client_secret'])
    socialapp.save()
    socialapp.sites.add( site )
    socialapp.save()
    return 


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", type=str, required=True, default=None,
                        help="configure file")
    args = parser.parse_args()
    config = json.load(open(args.config, 'r'))

    get_resource(config)
    upload_default(config)
    user_ids = generate_users(config)
    category_ids = generate_category(config)
    tag_ids = generate_tag(config)
    blog_ids = generate_blog(config, user_ids, category_ids, tag_ids)
    comment_ids = generate_comments(config, user_ids, blog_ids)
    follow_ids = generate_follow(config, user_ids)
    track_ids = generate_tracker(config, blog_ids)
    setup_social_account(config)

