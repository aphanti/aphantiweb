# aphanti web

## Dependencies

+ MySQL
    - Install MySQL on Mac: https://dev.mysql.com/doc/mysql-osx-excerpt/5.7/en/osx-installation.html
    - Install MySQL on Ubuntu: https://support.rackspace.com/how-to/install-mysql-server-on-the-ubuntu-operating-system/


+ Python libraries
    - mysql-connector-python: https://dev.mysql.com/doc/connector-python/en/connector-python-installation-binary.html
    - MySQLdb: pip install mysqlclient
    - django==3.0.0
    - python-memcached
    - six
    - markdown
    - Pillow
    - whitenoise
    - django-allauth
    - django-ckeditor
        + download the latest skin.js and put it in staticfiles/ckeditor/ckeditor/skins/moono/skin.js
        + delete staff_member_required() in anaconda3/lib/python3.7/site-packages/ckeditor_uploader/urls.py
            - or overwrite these two urls in aphantiweb/urls.py (before ckeditor's url)
    - django-widget-tweaks
    - django-social-share
    - geoip2: pip install geoip2
        + download geoip data files from: https://dev.maxmind.com/geoip/geoip2/geolite2/
    - django-tracking-analyzer: pip install django-tracking-analyzer
        + change anaconda3/lib/python3.7/site-packages/tracking_analyzer/bak_admin.py: line 200-208 to:
            ```python
            current_results = []
            objs = Tracker.objects.filter(pk__in=list(current_pks))
            for i in range(len(objs)):
                current_results.append({'date': objs[i].timestamp.isoformat()[:16], 'requests': i+1 })
            ```
    - user-agents:
        + pip install pyyaml ua-parser user-agents
        + pip install django-user-agents




## Quick Start

+ MySQL setting: 
    - Create the database in mysql and grant the permissions
        + CREATE USER 'newuser'@'localhost' IDENTIFIED BY 'user_password';
        + CREATE database 'database_name';
        + GRANT ALL PRIVILEGES ON database_name.* TO 'database_user'@'localhost';
    - Or dump the backuped SQL database to your mysql 

+ Gmail setting:
    - Turn on less secure apps: https://support.google.com/accounts/answer/6010255?hl=en
        + https://myaccount.google.com/lesssecureapps
    - Going to https://accounts.google.com/DisplayUnlockCaptcha to enable it (make sure you are using the right gmail acocunt ) and then retrying the operation


+ Credential setting: 
    - create /opt/aphanti/web_info.json which contains mysql, gmail pasword etc., like this:
    ```python
    {
        "domain_name": "127.0.0.1:8000", 
        "APHANTI_ENV": "dev",
        "APHANTI_SECRET_KEY": "xxx",
        "APHANTI_MYSQL_DBNAME": "aphantiweb",
        "APHANTI_MYSQL_USER": "aphanti",
        "APHANTI_MYSQL_PASSWORD": "xxx",
        "EMAIL_HOST_USER": "admin@aphanti.com",
        "EMAIL_HOST_PASSWORD": "xxx", 
        "GEOIP_PATH": "xxx", 
        "google_app_client_id": "xxx", 
        "google_app_client_secret": "xxx"
    }
    ```
    - on development machine: 
        + APHANTI_ENV should be "dev" 
        + domain_name should be "127.0.0.1:8000"
    - on deploy machine:
        + APHANTI_ENG = "prod"
        + domain_name = "www.aphanti.com"


+ Create simulated data in MySQL and run test 
    - cd test; sh test.sh


+ Build and run
    - sh run.sh


+ Enable google account signin
    - This part has been put into test/test.sh, so you don't need to do it manually
    - Tutorial: https://medium.com/@whizzoe/in-5-mins-set-up-google-login-to-sign-up-users-on-django-e71d5c38f5d5
    - Go to the admin@aphanti.com google developer console -> APIs credentials to get client ID and client secret (we have also saved them in web_info.json)
    - run makemigrations, migrate, and runserver on 127.0.0.1:8000
    - add site: -> Sites -> domain name: 127.0.0.1:8000
    - add client ID and secret key: -> Social applications:
        + Provider: Google
        + Name: Google API
        + Client id: xxx
        + Secrect key: xxx
        + Key: [secret key]
        + Sites: choose the domain (e.g. 127.0.0.1:8000)

+ copy skin.js to staticfiles/ckeditor/ckeditor/skins/moono/skin.js

+ On some machines, if the mysql doesn't support foreign languages, you will get 500 error when you create/update a blog with non-English words. In this case, run *test/support_unicode.py* to convert all the table to support unicode.
