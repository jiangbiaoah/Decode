# -*- coding: utf-8 -*-
import sqlite3
import pymysql
from function import mysql_qq_operate
from function import configuration
from function import encrypt

IMEI = "866574023790014"
imei = list(IMEI)
qq_db_path = "d:/2434601985.db"
qq_db_name = "2434601985"
qq_db_tablename = "mr_friend_B170D21B4A3EED531FE86C9B886F64C8_New"

friendlist = []

# 破解QQ步骤 qq_auto
# 1.获取用户手机QQ号，为该用户创建一个数据库--create_db(qqnum)
# 2.获取QQ群组信息
# 3.获取QQ好友列表信息
# 4.获取聊天记录信息

def qq_auto(qq_db_path, db_name, imei):
    result = mysql_qq_operate.create_db(db_name)   # 创建一个以qqnum为名的数据库
    if result == False:
        return
    store_qq_Groupsinfo(qq_db_path, qq_db_name, imei)
    store_qq_Friendsinfo(qq_db_path, qq_db_name, imei)
    store_qq_msgdata(qq_db_path, qq_db_name, imei, friendlist)

def store_qq_Groupsinfo(db_path, db_name, imei):
    # 将sqlite中QQ群组信息保存到mysql中
    tablename = "Groups"
    createresult = mysql_qq_operate.create_table(db_name, tablename)
    if createresult == False:
        return

    try:
        conn_sqlite = sqlite3.connect(db_path)
        c_sqlite = conn_sqlite.cursor()
        print("sqlite连接成功")

        conn_mysql = pymysql.connect(configuration.mysql_host, configuration.mysql_user, configuration.mysql_passwd,
                                     db_name, charset="utf8")
        c_mysql = conn_mysql.cursor()
        print("mysql连接成功")

        cursor_sqlite = c_sqlite.execute("SELECT * from Groups")
        for row in cursor_sqlite:
            id = row[0]
            group_name = encrypt.decrypted_use_xor(row[1], imei)
            group_id = row[2]
            group_friend_count = row[3]
            datetime = row[7]
            mysql_qq_operate.insert_into_Groups(c_mysql, id, group_name, group_id, group_friend_count, datetime)

        print("QQ群组信息保存完成")
        print("------------------------------------------------")
    except Exception as e:
        print("QQ群组信息保存出错")
        print(e)
        print("------------------------------------------------")

    conn_mysql.commit()
    conn_mysql.close()
    conn_sqlite.close()
    return

def store_qq_Friendsinfo(db_path, db_name, imei):
    # 将sqlite中QQ好友列表信息保存到mysql数据库中
    tablename = "Friends"
    createresult = mysql_qq_operate.create_table(db_name, tablename)
    if createresult == False:
        return

    try:
        conn_sqlite = sqlite3.connect(db_path)
        c_sqlite = conn_sqlite.cursor()

        conn_mysql = pymysql.connect(configuration.mysql_host, configuration.mysql_user, configuration.mysql_passwd,
                                     db_name, charset="utf8")
        c_mysql = conn_mysql.cursor()
        print("mysql连接成功")

        cursor_sqlite = c_sqlite.execute("SELECT * from Friends")
        for row in cursor_sqlite:
            _id = row[0]
            uin = encrypt.decrypted_use_xor(row[1], imei)
            remark = encrypt.decrypted_use_xor(row[2], imei)
            name = encrypt.decrypted_use_xor(row[3], imei)
            groupid = row[8]
            datetime = row[13]
            age = row[17]
            friendlist.append(uin)
            mysql_qq_operate.insert_into_Friends(c_mysql, _id, uin, remark, name, groupid, datetime, age)
        print("QQ好友信息保存成功")
        print("------------------------------------------------")
    except Exception as e:
        print("QQ好友信息保存失败")
        print(e)
        print("------------------------------------------------")
    conn_mysql.commit()
    conn_mysql.close()
    conn_sqlite.close()
    return

def store_qq_msgdata(db_path, db_name, imei, friendlist):
    # 将sqlite中QQ好友聊天记录信息保存到mysql数据库中
    if len(friendlist) == 0:
        print("error:好友列表为空")
        return
    # 获取所有mr_friend_***_New表
    try:
        conn_sqlite = sqlite3.connect(db_path)
        c_sqlite = conn_sqlite.cursor()

        conn_mysql = pymysql.connect(configuration.mysql_host, configuration.mysql_user, configuration.mysql_passwd,
                                     db_name, charset="utf8")
        c_mysql = conn_mysql.cursor()
        print("mysql连接成功")
    except Exception as e:
        print("sql连接失败")
        print(e)
        return

    sql_showtables = "SELECT name FROM sqlite_master WHERE type='table'"
    cursor_sqlite_showtables = c_sqlite.execute(sql_showtables).fetchall()
    # 遍历数据库中的所有表格，找出是聊天记录的表格
    friendlist_table = []
    for row_tables in cursor_sqlite_showtables:
        friendlist_table.append(row_tables[0])

    for friend_table in friendlist_table:
        for friend in friendlist:
            tablename = encrypt.get_tablename_by_QQnum(friend)
            if friend_table == tablename:
                print("与好友【%s】有聊天记录,表：%s" % (friend, tablename))
                tablename_new = "mr_friend_" + friend + "_New"
                createresult = mysql_qq_operate.create_table(db_name, tablename_new)
                if createresult == False:
                    return

                cursor_sqlite = c_sqlite.execute("SELECT * from %s" % tablename)
                for row in cursor_sqlite:
                    id = row[0]
                    msgData = encrypt.decrypted_Chinese_msgdata(row[13], imei)
                    time = row[22]
                    mysql_qq_operate.insert_into_tablename(c_mysql, tablename_new, id, msgData, time)
                print("好友【%s】聊天记录保存成功" % friend)
                print("------------------------------------------------")
            conn_mysql.commit()
    conn_mysql.close()
    conn_sqlite.close()
    return

store_qq_Groupsinfo(qq_db_path, qq_db_name, imei)
store_qq_Friendsinfo(qq_db_path, qq_db_name, imei)
store_qq_msgdata(qq_db_path, qq_db_name, imei, friendlist)

