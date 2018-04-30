# -*- coding: UTF-8 -*-

from function import configuration
import pymysql

# 创建用户数据库
# db_name:数据库名
def create_db(db_name):
    boolResult = False
    try:
        conn = pymysql.connect(configuration.mysql_host, configuration.mysql_user, configuration.mysql_passwd)
        c = conn.cursor()
        print("myql数据连接成功")
        print("准备创建数据库【%s】" % db_name)
        sql = "create database %s" % db_name
        c.execute(sql)
        print("mysql数据库[%s]创建成功" % db_name)
        boolResult = True
    except Exception as e:
        boolResult = False
        print("mysql数据库[%s]创建失败" % db_name)
        print(e)
    conn.close()
    print("------------------------------------------------")
    return boolResult

def create_table(db_name, tablename):
    boolResult = False
    try:
        conn = pymysql.connect(configuration.mysql_host, configuration.mysql_user, configuration.mysql_passwd,
                               db_name)
        c = conn.cursor()
        print("数据库连接成功")
        sql_drop = ""
        if tablename == "Friends":
            sql_drop = "drop table Friends"
        elif tablename == "Groups":
            sql_drop = "drop table Groups"
        elif tablename[0:9] == "mr_friend": # 以每个好友的QQ号为表名创建独立的表，tablename格式为：mr_friend_1584224172_New
            sql_drop = "drop table %s" % tablename
        else:
            return False
        c.execute(sql_drop)
        print("表[%s]已删除" % tablename)
    except:
        print("表[%s]删除失败" % tablename)

    try:
        sql_create = ""
        if tablename == "Friends":
            sql_create = """create table Friends(
                                                _id integer primary key ,
                                                uin text,
                                                remark text,
                                                name text,
                                                groupid integer,
                                                datetime text ,
                                                age integer )"""
        elif tablename == "Groups":
            sql_create = """create table Groups(
                                                id integer primary key ,
                                                group_name text,
                                                group_id integer ,
                                                group_friend_count integer ,
                                                datetime text )"""
        elif tablename[0:9] == "mr_friend":  # 以每个好友的QQ号为表名创建独立的表，tablename格式为：qqnum1584224172
            sql_create = """create table %s (
                                            id integer primary key ,
                                            msgData text ,
                                            time text )""" % tablename
        else:
            return False
        c.execute(sql_create)
        boolResult = True
        print("表[%s]创建成功" % tablename)
    except Exception as e:
        boolResult = False
        print("表[%s]创建失败" % tablename)
        print(e)
    conn.close()
    print("已关闭数据库连接")
    return boolResult

def insert_into_Groups(c, id, group_name, group_id, group_friend_count, datetime):
    try:
        sql = """insert into Groups values ('%d', '%s', '%d','%d','%d')""" % \
              (id, group_name, group_id, group_friend_count, datetime)
        c.execute(sql)
    except Exception as e:
        print(e)
        print("error in insert_into_Groups id = [%d]" % id)

def insert_into_Friends(c, _id, uin, remark, name, groupid, datetime, age):
    try:
        sql = """insert into Friends values ('%d', '%s', '%s', '%s', '%d','%d','%d')""" % \
              (_id, uin, remark, name, groupid, datetime, age)
        c.execute(sql)
    except Exception as e:
        print(e)
        print("error in insert_into_Friends _id = [%d]" % _id)

def insert_into_tablename(c, tablename, id, msgData, time):
    try:
        sql = """insert into %s values ('%d', '%s','%d')""" % \
              (tablename, id, msgData, time)
        c.execute(sql)
    except Exception as e:
        print(e)
        print("error in insert_into_%s id = [%d]" % (tablename, id))

