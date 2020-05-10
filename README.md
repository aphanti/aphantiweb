# aphanti web

## Quick Start

+ MySQL setting: 
    - Create the database in mysql and grant the permissions
        + CREATE USER 'newuser'@'localhost' IDENTIFIED BY 'user_password';
        + CREATE database 'database_name';
        + GRANT ALL PRIVILEGES ON database_name.* TO 'database_user'@'localhost';
    - Or dump the backuped SQL database to your mysql 

+ Gmail setting:
    - Turn on less secure apps: https://support.google.com/accounts/answer/6010255?hl=en
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
    - where APHANTI_ENV should be dev on your development computer, and prod on your deployment server



