## 使用方法：
## 引入database包
## 选择合适的语句复制，粘贴到需要插入数据位置，其中value为数据
## 水位：database.insertWaterData(value)
## 湿度：database.insertHumData(value)
## 温度：database.insertTempData(value)
import pymysql
import time
import random
# 打开数据库连接
def connect():
    db = pymysql.connect(host='127.0.0.1',
                         user='root',
                         password='123456',
                         database='iot')
    return db
 
# 使用cursor()方法获取操作游标
def insertWaterData(data):
    db = connect()
    cursor = db.cursor()
    wid = random.randint(1,9999999)
    date = time.strftime("%F %H:%M:%S")
    sql = "INSERT INTO waterData VALUES (%s, '%s', '%s')" % (wid, data, date)
    try:
       # 执行sql语句
       cursor.execute(sql)
       # 执行sql语句
       db.commit()
    except:
       # 发生错误时回滚
       print("error")
       db.rollback()
    # 关闭数据库连接
    db.close()
def insertTempData(data):
    db = connect()
    cursor = db.cursor()
    wid = random.randint(1,9999999)
    date = time.strftime("%F %H:%M:%S")
    sql = "INSERT INTO tempData VALUES (%s, '%s', '%s')" % (wid, data, date)
    try:
       # 执行sql语句
       cursor.execute(sql)
       # 执行sql语句
       db.commit()
    except:
       # 发生错误时回滚
       print("error")
       db.rollback()
    # 关闭数据库连接
    db.close()
def insertHumData(data):
    db = connect()
    cursor = db.cursor()
    wid = random.randint(1,9999999)
    date = time.strftime("%F %H:%M:%S")
    sql = "INSERT INTO humData VALUES (%s, '%s', '%s')" % (wid, data, date)
    try:
       # 执行sql语句
       cursor.execute(sql)
       # 执行sql语句
       db.commit()
    except:
       # 发生错误时回滚
       print("error")
       db.rollback()
    # 关闭数据库连接
    db.close()
if __name__ == "__main__":
    data = "2.3"
    insertWaterData(data)