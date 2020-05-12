import pandas as pd
import MySQLdb
import random
import squarify
import numpy as np
import os
import json 
import random 
from datetime import datetime, timedelta


def create_blogs(db, cursor):
    #cursor.execute('select * from blog_blog;')
    #out = cursor.fetchall()
    #table = [x[0] for x in cursor.fetchall()]
    #print(len(out), out)
    #cursor.execute(sql)

    author_ids = [2, 3]
    
    for i in range(60):
        map = {'id': 100+i, 'title':'title'+format(100+i), 
            'summary': 'summary'+format(100+i), 'body': 'body'+format(100+i), 
            'is_draft': random.choice([0,1]), 'author_id': random.choice(author_ids), 
            'create_time': (datetime(2020,5,1)+timedelta(days=i)).date().isoformat(), 
            'update_time': (datetime(2020,5,1)+timedelta(days=i)).date().isoformat(), 
            'publish_time': (datetime(2020,5,1)+timedelta(days=i)).date().isoformat(),  }

        cols = ','.join(['`'+x+'`' for x in list(map.keys())])
        values = ','.join(["'"+x+"'" if isinstance(x, str) else format(x) for x in list(map.values())])

        sql = "delete from blog_blog where id="+format(map['id'])+";"
        print(sql)
        cursor.execute(sql)

        sql = "INSERT INTO `blog_blog` ("+cols+") VALUES ("+values+");"
        print(sql)
        cursor.execute(sql)

    db.commit()

    return

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--app", type=str, required=False, default=None,
                        help="app name")
    parser.add_argument("-t", "--table", type=str, required=False, default=None,
                        help="table name")
    args = parser.parse_args()

    web_info = json.load(open('/opt/aphanti/web_info.json', 'r'))
    user = web_info['APHANTI_MYSQL_USER']
    host = "localhost"
    passwd = web_info['APHANTI_MYSQL_PASSWORD']
    dbname = web_info['APHANTI_MYSQL_DBNAME']
    db = MySQLdb.connect(host=host, user=user, passwd=passwd, db=dbname)
    cursor = db.cursor()

    create_blogs(db, cursor)

