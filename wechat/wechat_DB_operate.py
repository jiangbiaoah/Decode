# -*- coding: utf-8 -*-

from function import mysql_wechat_operate
from function import configuration
import sqlite3
import pymysql

def wechat_auto(db_path):
    store_wechat_friendsinfo(db_path)
    store_wechat_friendsinfo(db_path  )

def store_wechat_friendsinfo(db_path):
    # 将sqlite中的微信好友信息存储到mysql中
    # db_path :sqlite中微信数据库的路径，及EnMicroMsg_decrypted.db的路径
    db_name = "wechat"
    tablename = "rcontact"
    creattable = mysql_wechat_operate.create_table(db_name, tablename)  # 若数据库wechat中已存在rcontact则删除，并重建

    conn_sqlite = sqlite3.connect(db_path)
    c_sqlite = conn_sqlite.cursor()
    cursor_sqlite = c_sqlite.execute("select * from rcontact")

    conn_mysql = pymysql.connect(configuration.mysql_host, configuration.mysql_user, configuration.mysql_passwd,
                                 db_name, charset="utf8")
    c_mysql = conn_mysql.cursor()

    for row in cursor_sqlite:   # 将sqlite中指定数据以相同格式存储到mysql
        username = row[0]
        alias = row[1]
        conRemark = row[2]
        nickname = row[4]
        pyInitial = row[5]
        quanPin = row[6]
        showHead = row[7]
        mysql_wechat_operate.insert_into_rcontact(c_mysql, username, alias, conRemark, nickname, pyInitial, quanPin, showHead)

    conn_mysql.commit()
    conn_mysql.close()
    conn_sqlite.close()

def store_wechat_message(db_path):
    # 将sqlite中的微信好友聊天记录信息存储到mysql中
    # db_path :sqlite中微信数据库的路径，及EnMicroMsg_decrypted.db的路径
    db_name = "wechat"
    tablename = "message"
    mysql_wechat_operate.create_table(db_name, tablename)

    conn_sqlite = sqlite3.connect(db_path)
    c_sqlite = conn_sqlite.cursor()
    cursor_sqlite = c_sqlite.execute("select * from message")

    conn_mysql = pymysql.connect(configuration.mysql_host, configuration.mysql_user, configuration.mysql_passwd,
                                 db_name, charset="utf8")
    c_mysql = conn_mysql.cursor()

    for row in cursor_sqlite:
        msgId = row[0]
        msgSvrId = row[1]
        createtime = row[6]
        talker = row[7]
        content = row[8]
        imgPath = row[9]
        talkerId = row[14]
        msgSeq = row[18]
        mysql_wechat_operate.insert_into_message(c_mysql, msgId, msgSvrId, createtime, talker, content, imgPath, talkerId, msgSeq)

    conn_mysql.commit()
    conn_mysql.close()
    conn_sqlite.close()
