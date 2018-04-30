# -*- coding: UTF-8 -*-

from function import configuration
import pymysql

def create_table(databasename, tablename):
    boolResult = False
    try:
        conn = pymysql.connect(configuration.mysql_host, configuration.mysql_user, configuration.mysql_passwd,
                               databasename)
        c = conn.cursor()
        print("数据库连接成功")
        sql_drop = ""
        if tablename == "rcontact":
            sql_drop = "drop table rcontact"
        elif tablename == "message":
            sql_drop = "drop table message"
        else:
            return False
        c.execute(sql_drop)
        print("表[%s]已删除" % tablename)
    except:
        print("表[%s]删除失败" % tablename)

    try:
        sql_create = ""
        if tablename == "rcontact":
            sql_create = """create table rcontact(
                                                username char(50) primary key ,
                                                alias char(50),
                                                conRemark char(20),
                                                nickname varchar(255),
                                                pyInitial varchar(255),
                                                quanPin varchar(255),
                                                showHead integer )"""
        elif tablename == "message":
            sql_create = """create table message(
                                                msgId integer primary key,
                                                msgSvrId varchar(255),
                                                createtime varchar(255),
                                                talker text,
                                                content text,
                                                imgPath text,
                                                talkerId integer,
                                                msgSeq text )"""
        else:
            return False
        c.execute(sql_create)
        boolResult = True
        print("表[%s]创建成功" % tablename)
    except:
        boolResult = False
        print("表[%s]创建失败" % tablename)
    conn.close()
    print("已关闭数据库连接")
    return boolResult

def insert_into_rcontact(c, username, alias, conRemark, nickname, pyInitial, quanPin, showHead):
    try:
        sql = """insert into rcontact(username, alias, conRemark, nickname, pyInitial, quanpin, showHead)
                    values ('%s', '%s', '%s', '%s', '%s', '%s', '%d')""" % \
              (username, alias, conRemark, nickname, pyInitial, quanPin, showHead)
        c.execute(sql)
    except:
        print("error in insert_into_rcontact username = [%s]" % username)

def insert_into_message(c, msgId, msgSvrId, createtime, talker, content, imgPath, talkerId, msgSeq):
    try:
        sql = """insert into message(msgId, msgSvrId, createtime, talker, content, imgPath, talkerId, msgSeq)
                    values ('%d','%s','%s','%s','%s','%s','%d','%s')""" % \
              (msgId, msgSvrId, createtime, talker, content, imgPath, talkerId, msgSeq)
        c.execute(sql)
    except Exception as e:
        print(e)
        print("error in insert_into_message msgId = [%s]" % msgId)

