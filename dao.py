import re
import struct

import MySQLdb
# 打开数据库连接
from sqlalchemy import null

# db = MySQLdb.connect("localhost", "root", "123456", "SinaSpider", charset='utf8' )# 调试使用的数据库
db = MySQLdb.connect("localhost", "root", "123456", "SinaSpider", charset='utf8' )# 调试使用的数据库

# 使用cursor()方法获取操作游标
cursor = db.cursor()

def create_table(topic):
    '''
    建表语句
    :param topic:
    :return:
    '''
    # 如果数据表已经存在使用 execute() 方法删除表。
    sql = f"""DROP TABLE IF EXISTS {topic}"""
    print(sql)
    cursor.execute(sql)

    # 创建数据表SQL语句
    sql = f"""CREATE TABLE {topic} (
             user  CHAR(20) PRIMARY KEY NOT NULL,
             content BLOB
             )"""
    print(sql)
    #blob
    cursor.execute(sql)
    # 关闭数据库连接
    print('******************************建表成功！*********************************')
    # db.close()



def insert(topic,user,content):
    # SQL 插入语句
    sql = f"""INSERT INTO {topic} (user, content) values(%s, %s)"""
    #执行sql语句
    # user = eval(user)
    # print("user:"+user+'\n'+"text:"+content)
    try:
        cursor.execute(sql, (user,content))
        # cursor.execute(sql, (MySQLdb.Binary(user)))

        # cursor.execute(sql)
        # 提交到数据库执行
        db.commit()

        print('*********************************插入成功！************************************                         已插入数据：'+ str(total(topic)))
    except:
        # 数据库 用户名是主键，每个用户的微博只保存一次，所以有重复数据时，会插入失败，用此方法处理重复数据有待改进
        #Rollback in case there is any error
        # print('******************************插入失败，回滚！*********************************')
        db.rollback()


# def write_num():
#     '''
#     把爬取的内容条目保存成文件，下次接着计数，因直接用数据库查询语句统计条目，方法弃用，在后续的算法改进时可考虑此方法
#     :return:
#     '''
#
#     with open('num.ini', 'w', encoding='utf-8') as f:
#         f.write(num)


def read_num():

    '''
    读文件,程序调试使用
    '''

    try:
        f = open('num.ini', 'r', encoding='utf-8')
        now_num = f.read()
    except:
        print('文件读取错误！')
    finally:
        if f:
            f.close()
    return now_num


def closeDB():
    '''
    关闭数据库
    :return:
    '''
    db.close()

def table_exists(table_name):
    #这个函数用来判断表是否存在
    sql = "show tables;"
    cursor.execute(sql)
    tables = [cursor.fetchall()]
    table_list = re.findall('(\'.*?\')',str(tables))
    table_list = [re.sub("'", '', each) for each in table_list]
    if table_name in table_list:
        return 1#存在返回1
    else:
        return 0

def total(topic):
    '''
    统计插入条目，因频繁访问数据库，此方法要改进
    :param topic: 关键词
    :return: 返回统计结果
    '''

    sql = f'SELECT COUNT(user) FROM {topic}'
    cursor.execute(sql)
    total = 0
    result = cursor.fetchall()
    for row in result:
        total = row[0]
    return total


def select_ALL(topic):
    '''
    查询数据库所有条目 调试使用
    :param topic:
    :return:
    '''

    # SQL 查询语句
    sql = f"SELECT * FROM {topic}"
    print(sql)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            user = row[0]
            text = row[1]
            text = text.decode('utf-8')

            # 打印结果
            print(user)
            print(text)

    except:
        print("**************************查询数据失败！*****************************")
    # 关闭数据库连接
    db.close()


def getContent(topic):
    '''
    将数据库中的数据取出
    :param topic: 要查询的关键词
    :return: 查询结果
    '''
    db = MySQLdb.connect("localhost", "root", "123456", "sinaspider", charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    sql = f"SELECT * FROM {topic}"
    weiboUser = []
    weiboText = []
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            user = row[0]
            text = row[1]
            text = text.decode('utf-8')
            weiboUser.append(user)
            weiboText.append(text)
    except:
        print("**************************查询数据失败！*****************************")
    # 关闭数据库连接
    db.close()
    content = [weiboUser,weiboText]
    return content

