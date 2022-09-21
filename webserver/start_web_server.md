#scan ports
netstat -a

# uninstall apache
sudo service apache2 stop
sudo apt-get purge apache2 apache2-utils apache2.2-bin apache2-common
sudo apt-get autoremove
whereis apache2
sudo rm -rf /etc/apache2

# install apache
sudo apt update
sudo apt install apache2
sudo ufw allow 'Apache'
sudo ufw app list
sudo ufw status
sudo systemctl status apache2

sudo systemctl stop apache2
sudo systemctl start apache2
sudo systemctl restart apache2
sudo systemctl reload apache2
sudo systemctl disable apache2
sudo systemctl enable apache2
sudo service apache2 restart
sudo service apache2 stop
sudo service apache2 start

# virtual host
vim /etc/apache2/sites-available/example.com.conf

<VirtualHost *:80>
    ServerAdmin admin@example.com
    ServerName example.com
    ServerAlias www.example.com
    DocumentRoot /var/www/example.com/html
    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>

sudo a2ensite example.com.conf
sudo a2dissite 000-default.conf
sudo apache2ctl configtest
sudo systemctl restart apache2
sudo service apache2 restart

# install wsgi module
sudo apt-get install libapache2-mod-wsgi-py3
sudo a2enmod wsgi
sudo service apache2 restart

# To use https:
# 1. install certbot
sudo apt-get install python-certbot-apache
sudo certbot --apache -d www.example.com
# if "duplicate wsgi error" appears, comment out the wsgi in the config and rerun this command, and finally remember uncomment them in the ssl config
sudo certbot renew --dry-run

# 2. then add wsgi config in example.com-le-ssl.conf, for example:
    WSGIDaemonProcess example.com processes=1 threads=5 python-home=/home/oscar/django/myweb/venv python-path=/home/oscar/django/myweb
    WSGIProcessGroup example.com
    WSGIScriptAlias / /home/oscar/django/myweb/myweb/wsgi.py

    Alias /static /home/oscar/django/myweb/staticfiles
    <Directory /home/oscar/django/myweb/staticfiles>
        Require all granted
    </Directory>

    Alias /media /home/oscar/django/myweb/uploads
    <Directory /home/oscar/django/myweb/uploads>
        Require all granted
    </Directory>

    <Directory /home/oscar/django/myweb/myweb>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>

# 3. restart apache2
sudo service apache2 restart

# if you use your home ip to host the domain, make sure you have the right port forward:
#    if http: 80 -> 80
#    if https: 443 -> 443


