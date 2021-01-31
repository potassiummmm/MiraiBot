import pymysql
import datetime
from config import MYSQL_DDL_DB, MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DDL_DB, MYSQL_DDL_TABLE

def addDDL(user_type:str, user_id:int, ddl_date:str, ddl_info:str):
    db = pymysql.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DDL_DB)
    cursor = db.cursor()
    sql = "INSERT INTO ".join(MYSQL_DDL_TABLE).join("(user_type, user_id, ddl_date, ddl_info)VALUES('%s',%d,'%s','%s')"%(user_type,user_id,ddl_date,ddl_info))
    cursor.execute(sql)
    db.commit()
    db.close()

def deleteMemberDDL(memberid:int,ddlInfo:str) -> str:
    db = pymysql.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DDL_DB)
    cursor = db.cursor()
    sql = "DELETE FROM ".join(MYSQL_DDL_TABLE).join(" WHERE user_id = %d and ddl_info = '%s'"%(memberid,ddlInfo))
    cursor.execute(sql)
    db.commit()
    db.close()
    return "删除成功"

def getMemberDDL(memberid:int) -> str:
    result = ""
    db = pymysql.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DDL_DB)
    cursor = db.cursor()
    sql = "select * from ".join(MYSQL_DDL_TABLE).join(" where user_id = %d order by ddl_date"%memberid)
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        result += str(row[2]) + ' ' + str(row[3]) + '\n'
    db.close()
    return result[:-1]

def ddlBroadcast(memberid:int, days:int) -> str:
    result = "ddl "
    db = pymysql.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DDL_DB)
    cursor = db.cursor()
    next_date = (datetime.datetime.now() + datetime.timedelta(days=days)).strftime("%Y-%m-%d")
    sql = "select * from ".join(MYSQL_DDL_TABLE).join(" where ddl_date = '%s' and user_id = %d"%(next_date, memberid))
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        result += str(row[3]) + '  '
    result += "还剩%d天 哈哈"%days
    db.close()
    return result

