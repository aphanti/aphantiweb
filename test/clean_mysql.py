import pandas as pd
import MySQLdb
import random
import squarify
import numpy as np
import os
import json 


def drop_all_tables(db, cursor):
    cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
    cursor.execute('show tables;')
    tables = [x[0] for x in cursor.fetchall()]
    for table in tables:
        sql = "drop table " + table + ";"
        print(sql);
        cursor.execute(sql)
    db.commit()
    return    


def clear_mysql(db, cursor, app, table):
    if table is not None:
        sql = "delete from `auth_permission` where `name` like '%"+table+"%';";
        print(sql);
        cursor.execute(sql)
        sql = "delete from `django_content_type` where `model` = '"+table+"';";
        print(sql);
        cursor.execute(sql)
        db.commit()
    
    if app is not None:
        cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
        cursor.execute('show tables;')
        tables = [x[0] for x in cursor.fetchall()]
        for table in tables:
            if app+'_' in table:
                sql = "drop table " + table + ";"
                print(sql);
                cursor.execute(sql)

        sql = "delete from `django_migrations` where `app` = '"+app+"';";
        print(sql)
        cursor.execute(sql)
        sql = "delete from `auth_permission` where `name` like '%"+app+"%';";
        print(sql)
        cursor.execute(sql)
        sql = "delete from `django_content_type` where `app_label` = '"+app+"';";
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
    parser.add_argument("--drop_all", action='store_true', required=False, default=False,
                        help="drop all tables")

    args = parser.parse_args()

    web_info = json.load(open('/opt/aphanti/web_info.json', 'r'))
    user = web_info['APHANTI_MYSQL_USER']
    host = "localhost"
    passwd = web_info['APHANTI_MYSQL_PASSWORD']
    dbname = web_info['APHANTI_MYSQL_DBNAME']
    db = MySQLdb.connect(host=host, user=user, passwd=passwd, db=dbname)
    cursor = db.cursor()

    if args.drop_all:
        drop_all_tables(db, cursor)
    else:
        clear_mysql(db, cursor, args.app, args.table)

