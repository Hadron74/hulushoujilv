# -*-coding:utf-8-*-
__author__ = 'luhongc'

import MySQLdb


def connect():
    return connect_localhost()


def connect_localhost():
    conn = MySQLdb.connect(host="localhost", user="root",
                           passwd="", db="hulushoujilv", charset='utf8')
    return conn


def create_sql(conn):
    cur = conn.cursor()

    cur.execute("""create table if not exists REPLY (ID bigint not null,
                        IP VARCHAR(40) not null,
                        NC VARCHAR(40) not null,
                        TI DATETIME not null,
                        TE TEXT not null,
                        UD bigint not null,
                        primary key (ID))charset = utf8;""" + "\n")
    cur.execute("""create table if not exists LINKS (ROOTID bigint not null,
                        REPLYID bigint not null,
                        primary key (REPLYID));""" + "\n")

    cur.execute("""create table if not exists REPLYTAG (ID bigint not null,
                        CLASS int,
                        KEYWORD text,
                        primary key (ID))charset = utf8;""" + "\n")

    cur.execute("""create table if not exists KEYWORD (ID bigint not null,
                        KEYWORD VARCHAR(256),
                        primary key (ID))charset = utf8;""" + "\n")

    cur.execute("""create table if not exists CLASS (ID bigint not null,
                        NAME VARCHAR(256),
                        primary key (ID))charset = utf8;""" + "\n")


def select_reply(conn, id):
    sql = "select * from reply where ID = %s; "
    cur = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    cur.execute(sql, str(id))
    rst = cur.fetchone()
    return rst


def select_link_reply(conn, id):
    sql = "select * from links where REPLYID = %s; "
    cur = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    cur.execute(sql, str(id))
    return cur.fetchone()


def select_link_root(conn, id):
    sql = "select * from links where ROOTID = %s; "
    cur = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    cur.execute(sql, str(id))
    return cur.fetchall()


def insert_reply(conn, id, sql):
    if select_reply(conn, id) is None:
        try:
            cur = conn.cursor()
            print "SSSSSSSSSS", sql
            cur.execute(sql)
            conn.commit()
            return "SUCCESS"
        except:
            conn.rollback()
    return


def insert_link(conn, id, sql):
    if select_link_reply(conn, id) is None:
        try:
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()
            return "SUCCESS"
        except:
            conn.rollback()
    return


if __name__ == "__main__":
    conn = connect()
    create_sql(conn)
    conn.close()
