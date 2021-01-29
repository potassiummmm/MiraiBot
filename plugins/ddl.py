import pymysql
import datetime

def addDDL(user_type:str, user_id:int, ddl_date:str, ddl_info:str):
    db = pymysql.connect("localhost", "root", "potassium", "ddl_db")
    cursor = db.cursor()
    sql = "INSERT INTO ddl_table(user_type, user_id, ddl_date, ddl_info)VALUES('%s',%d,'%s','%s')"%(user_type,user_id,ddl_date,ddl_info)
    cursor.execute(sql)
    db.commit()
    db.close()

def deleteMemberDDL(memberid:int,ddlInfo:str) -> str:
    db = pymysql.connect("localhost", "root", "potassium", "ddl_db")
    cursor = db.cursor()
    sql = "DELETE FROM ddl_table WHERE user_id = %d and ddl_info = '%s'"%(memberid,ddlInfo)
    cursor.execute(sql)
    db.commit()
    db.close()
    return "删除成功"

def getMemberDDL(memberid:int) -> str:
    result = ""
    db = pymysql.connect("localhost", "root", "potassium", "ddl_db")
    cursor = db.cursor()
    sql = "select * from ddl_table where user_id = %d order by ddl_date"%memberid
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        result += str(row[2]) + ' ' + str(row[3]) + '\n'
    db.close()
    return result[:-1]

def ddlBroadcast(memberid:int, days:int) -> str:
    result = "ddl "
    db = pymysql.connect("localhost", "root", "potassium", "ddl_db")
    cursor = db.cursor()
    next_date = (datetime.datetime.now() + datetime.timedelta(days=days)).strftime("%Y-%m-%d")
    sql = "select * from ddl_table where ddl_date = '%s' and user_id = %d"%(next_date, memberid)
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        result += str(row[3]) + '  '
    result += "还剩%d天 哈哈"%days
    db.close()
    return result

