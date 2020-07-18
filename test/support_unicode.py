#! /usr/bin/env python
import MySQLdb
import json 


def change_to_support_unicode(dbname, user, passwd):
    host = "localhost"

    db = MySQLdb.connect(host=host, user=user, passwd=passwd, db=dbname)
    cursor = db.cursor()

    cursor.execute("ALTER DATABASE `%s` CHARACTER SET 'utf8' COLLATE 'utf8_unicode_ci'" % dbname)

    sql = "SELECT DISTINCT(table_name) FROM information_schema.columns WHERE table_schema = '%s'" % dbname
    print(sql)
    cursor.execute(sql)

    results = cursor.fetchall()
    for row in results:
        sql = "ALTER TABLE `%s` convert to character set DEFAULT COLLATE DEFAULT" % (row[0])
        print(sql)
        cursor.execute(sql)
        #db.commit()
    db.close()

    return 


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", type=str, required=False, default='/opt/aphanti/web_info.json',
                        help="path of web_info.json")
    args = parser.parse_args()

    web_info = json.load(open(args.config, 'r'))
    change_to_support_unicode(web_info['APHANTI_MYSQL_DBNAME'], 
        web_info['APHANTI_MYSQL_USER'], web_info['APHANTI_MYSQL_PASSWORD'])
