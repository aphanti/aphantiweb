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

proj_dir = os.path.dirname(os.path.abspath(__file__)) + '/../'
sys.path.append( proj_dir )
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aphantiweb.settings')
django.setup()  

from accounts.models import WebUser
from blog.models import Blog, Comment, Category, Tag, Follow
from subscribe.models import SubscribeList


resource_names = []
resource_words = []
resource_images = []



def get_resource(config):
    global resource_names, resource_words, resource_images
    print('get resources')
    resource_names = list(set([line.strip() for line in open(config['user_name'], 'r').readlines() if len(line.strip())>0]))
    resource_words = [line.strip() for line in open(config['words'], 'r').readlines() if len(line.strip())>0]
    resource_images = glob.glob(config['random_image']+'/*')
    return 


def upload_default(config):
    os.system('mkdir -p '+proj_dir+'/uploads/user_avatar')
    os.system('cp -f resource/user_avatar_default.jpg '+proj_dir+'/uploads/user_avatar/default.jpg')
    os.system('mkdir -p '+proj_dir+'/uploads/blog_category')
    os.system('cp -f resource/category_bg_default.jpg '+proj_dir+'/uploads/blog_category/default.jpg')
    os.system('mkdir -p '+proj_dir+'/uploads/blog_body_image')


def get_database_connection(config):
    print('get database connected')
    web_info = json.load(open(config['web_info'], 'r'))
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
    user.save() 
    ids.append(user.id)

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
        user.is_verified = True
        if random.random() < config['user_has_avatar_prob']:
            fsource = random.choice(resource_images)
            fsave = format(user.id)+'.avatar'
            os.system('cp -f '+fsource+' '+proj_dir+'/uploads/user_avatar/'+fsave)
            user.avatar = 'user_avatar/'+fsave
        bio_length = random.choice(range(config['bio_length_range'][0], config['bio_length_range'][1]))
        if bio_length > 0:
            user.bio = ' '.join( random.choices(resource_words, k=bio_length) )
        user.save() 
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

    time0 = datetime.strptime(config['blog_time_range'][0], "%Y-%m-%d")
    time1 = datetime.strptime(config['blog_time_range'][1], "%Y-%m-%d")
    dt = time1-time0
    dsecond = 1.0*(dt.days*86400 + dt.seconds)

    ids = []
    npic = 0
    for i in range(config['num_blog']):
        print('generate blog', i+1)
        blog = Blog( id=i+1, author_id = random.choice(user_ids), 
            category_id = random.choice(category_ids), 
            is_draft = random.choice([True, False]) )
        blog.save()
        ntag = random.choice( range(config['blog_tag_range'][0], config['blog_tag_range'][1]) )
        if ntag > 0:
            for itag in random.sample( tag_ids, ntag ):
                blog.tag.add( Tag.objects.get(pk = itag) )
        blog.title = get_random_sentence(config['blog_title_length_range'])
        blog.summary = get_random_sentence(config['blog_summary_length_range'])
        blog.create_time = time0 + timedelta(seconds = int(1.0*random.random()*dsecond))
        blog.publish_time = blog.create_time + timedelta(days = 1)
        blog.update_time = blog.create_time + timedelta(days = 2)
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
        ids.append(blog.id)

    return ids 


def generate_comments(config, user_ids, blog_ids):
    print('--- delete all comments ---')
    Comment.objects.all().delete()

    time0 = datetime.strptime(config['blog_time_range'][0], "%Y-%m-%d")
    time1 = datetime.strptime(config['blog_time_range'][1], "%Y-%m-%d")
    dt = time1-time0
    dsecond = 1.0*(dt.days*86400 + dt.seconds)

    ids = []
    for i in range(config['num_comment']): 
        print('generate comment:', i+1)
        comment = Comment(id=i+1, blog_id = random.choice(blog_ids), 
            author_id = random.choice(user_ids), 
            content = get_random_sentence(config['comment_length_range']))
        comment.create_time = time0 + timedelta(seconds = int(1.0*random.random()*dsecond))
        comment.save()
        ids.append(comment.id)
    
    return ids 


def generate_follow(config, user_ids):
    print('--- delete all follows ---')
    Follow.objects.all().delete()

    time0 = datetime.strptime(config['blog_time_range'][0], "%Y-%m-%d")
    time1 = datetime.strptime(config['blog_time_range'][1], "%Y-%m-%d")
    dt = time1-time0
    dsecond = 1.0*(dt.days*86400 + dt.seconds)

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


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", type=str, required=True, default=None,
                        help="configure file")
    args = parser.parse_args()
    config = json.load(open(args.config, 'r'))


    get_resource(config)
    upload_default(config)
    #db = get_database_connection(config)
    user_ids = generate_users(config)
    category_ids = generate_category(config)
    tag_ids = generate_tag(config)
    blog_ids = generate_blog(config, user_ids, category_ids, tag_ids)
    comment_ids = generate_comments(config, user_ids, blog_ids)
    follow_ids = generate_follow(config, user_ids)

