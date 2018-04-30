# -*- coding: utf-8 -*-
import hashlib


def __encrypt_use_MD5(str):
    # 创建md5对象
    hl = hashlib.md5()
    hl.update(str.encode(encoding='utf-8'))
    str_encrypted = hl.hexdigest()
    return str_encrypted

def get_tablename_by_QQnum(qqNum):
    # 根据QQ号获取MD5加密后的聊天记录表名"mr_friend_B170D21B4A3EED531FE86C9B886F64C8_New"
    qqNum_MD5 = __encrypt_use_MD5(qqNum).upper()
    tablename = "mr_friend_%s_New" % qqNum_MD5
    return tablename

def decrypted_use_xor(str, imei):
    # 异或解密，返回解密后的明文
    group_name_decode = ''
    if str == None:
        return group_name_decode
    for i in range(0, len(str)):
        group_name_decode += chr(ord(str[i]) ^ ord(imei[i % 15]))
    return group_name_decode

def decrypted_English_msgdata(msgdata_original, imei):
    # 解码英文二进制编码：输入加密的二进制消息和IMEI，返回明文
    # msgdata_original:源二进制消息
    msgdata_str = ""  # 解密后的数据
    try:
        msgdata_decode = msgdata_original.decode("utf-8")  # 解码后的数据
        for i in range(0, len(msgdata_decode)):
            msgdata_str += chr(ord(msgdata_decode[i]) ^ ord(imei[i % 15]))  # 异或解密
    except:
        msgdata_str = "--"
    # print("明文：", msgdata_str)
    return msgdata_str

def decrypted_Chinese_msgdata(msgdata_original, imei):
    # 解码中文二进制编码：输入加密的二进制消息和IMEI，返回明文
    # msgdata_original:源二进制消息
    try:
        msgdata_decode_binary_str = "" # 解码后的字符串格式的二进制数据
        for i in range(0, len(msgdata_original)):
            middle_result_hex = hex(int(hex(msgdata_original[i]), 16) ^ ord(imei[i % 15]))
            msgdata_decode_binary_str += str(middle_result_hex)
        # print("msgdata_decode_binary_str = ", msgdata_decode_binary_str)
        str_a = msgdata_decode_binary_str.replace('0x', '\\x')      # 0xe50x8f0x88 ->\xe5\x8f\x88
        str_b = "b'"+str_a + "'"                                    # \xe5\x8f\x88 ->b'\xe5\x8f\x88'
        msgdata_decode_str = eval(str_b).decode('utf-8')            # b'\xe5\x8f\x88' -> 兄
        # print("明文：", msgdata_decode_str)
    except Exception as e:
        msgdata_decode_str = "error in decrypted"
        print(e)

    return msgdata_decode_str
