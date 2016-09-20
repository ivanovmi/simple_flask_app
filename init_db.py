import MySQLdb as db


def main():
    conn = db.connect(user='flaskuser')
    cur = conn.cursor()
    print 'Drop flaskapp db'
    sql_query = 'DROP DATABASE IF EXISTS flaskapp;'
    cur.execute(sql_query)
    print 'Create flaskapp db'
    sql_query = 'CREATE DATABASE flaskapp CHARACTER SET utf8; USE flaskapp;'
    cur.execute(sql_query)
    print 'Create organizer table'
    sql_query = 'CREATE TABLE organizer(id int NOT NULL AUTO_INCREMENT, text TEXT(500), date DATE, done BOOL, PRIMARY KEY(id), FULLTEXT idx (text));'
    cur.execute(sql_query)

if __name__ == '__main__':
    main()