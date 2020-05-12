# aphanti web

## Dependencies

+ MySQL
    - Install MySQL on Mac: https://dev.mysql.com/doc/mysql-osx-excerpt/5.7/en/osx-installation.html
    - Install MySQL on Ubuntu: https://support.rackspace.com/how-to/install-mysql-server-on-the-ubuntu-operating-system/


+ Python libraries
    - mysql-connector-python: https://dev.mysql.com/doc/connector-python/en/connector-python-installation-binary.html
    - MySQLdb
    - django
    - whitenoise
    - django-allauth
    - django-ckeditor
    - django-widget-tweaks



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
        "APHANTI_ENV": "dev",
        "APHANTI_SECRET_KEY": "xxx",
        "APHANTI_MYSQL_DBNAME": "aphantiweb",
        "APHANTI_MYSQL_USER": "aphanti",
        "APHANTI_MYSQL_PASSWORD": "xxx",
        "EMAIL_HOST_USER": "admin@aphanti.com",
        "EMAIL_HOST_PASSWORD": "xxx"
    }
    ```
    - where APHANTI_ENV should be "dev" on your development computer, and "prod" on your deployment server


+ Create simulated data in MySQL
    - cd test; python3 generate_data.py -c config.json


+ Build and run
    - sh run.sh


+ Enable google account signin
    - Tutorial: https://medium.com/@whizzoe/in-5-mins-set-up-google-login-to-sign-up-users-on-django-e71d5c38f5d5
    - Go to the admin@aphanti.com google developer console -> APIs credentials to get client ID and client secret (we also save them in web_info.json)
    - run makemigrations, migrate, and runserver on 127.0.0.1:8000
    - add site: -> Sites -> domain name: 127.0.0.1:8000
    - add client ID and secret key: -> Social applications:
        + Provider: Google
        + Name: Google API
        + Client id: xxx
        + Secrect key: xxx
        + Key: [secret key]
        + Sites: choose the domain (e.g. 127.0.0.1:8000)
