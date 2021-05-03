from graia.application.entry import GraiaMiraiApplication, Group, Member, MessageChain, Plain
from graia.scheduler.timers import crontabify
from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DDL_DB, MYSQL_DDL_TABLE
from core import Instance
import pymysql
import datetime


def addDDL(user_type: str, user_id: int, ddl_date: str, ddl_info: str):
    db = pymysql.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DDL_DB)
    cursor = db.cursor()
    sql = "INSERT INTO " + MYSQL_DDL_TABLE + "(user_type, user_id, ddl_date, ddl_info)VALUES('%s',%d,'%s','%s')" % (
        user_type, user_id, ddl_date, ddl_info)
    cursor.execute(sql)
    db.commit()
    db.close()


def deleteMemberDDL(memberid: int, ddlInfo: str) -> str:
    db = pymysql.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DDL_DB)
    cursor = db.cursor()
    sql = "DELETE FROM " + MYSQL_DDL_TABLE + " WHERE user_id = %d and ddl_info = '%s'" % (memberid,
                                                                                          ddlInfo)
    cursor.execute(sql)
    db.commit()
    db.close()
    return "删除成功"


def getMemberDDL(memberid: int) -> str:
    result = ""
    db = pymysql.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DDL_DB)
    cursor = db.cursor()
    sql = "select * from " + MYSQL_DDL_TABLE + " where user_id = %d order by ddl_date" % memberid
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        result += str(row[2]) + ' ' + str(row[3]) + '\n'
    db.close()
    return result[:-1]


def ddlBroadcast(memberid: int, days: int) -> str:
    result = "ddl "
    db = pymysql.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DDL_DB)
    cursor = db.cursor()
    next_date = (datetime.datetime.now() + datetime.timedelta(days=days)).strftime("%Y-%m-%d")
    sql = "select * from " + MYSQL_DDL_TABLE + " where ddl_date = '%s' and user_id = %d" % (
        next_date, memberid)
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        result += str(row[3]) + '  '
    result += "还剩%d天 哈哈" % days
    db.close()
    return result


sche = Instance.sche()
bcc = Instance.bcc()


@sche.schedule(crontabify("0 8 * * *"))
async def ddl_week_scheduler():
    pass


@bcc.receiver("GroupMessage")
async def group_message_listener(app: GraiaMiraiApplication, group: Group, message: MessageChain,
                                 member: Member):
    if message.asDisplay().lower().startswith("ddl"):
        msg_list = message.asDisplay().split(' ')
        if msg_list[1] == 'add':
            if msg_list[2] == 'g':
                addDDL("group", group.id, msg_list[3], msg_list[4])
            else:
                addDDL("member", member.id, msg_list[2], msg_list[3])
        elif msg_list[1] == 'help':
            await app.sendGroupMessage(
                group, MessageChain.create([Plain("ddl+add+(g)+date+info添加ddl,g表示group")]))
        elif msg_list[1] == 'rm':
            if msg_list[2] == 'g':
                deleteMemberDDL(group.id, msg_list[3])
            else:
                deleteMemberDDL(member.id, msg_list[2])
        elif msg_list[1] == 'show':
            result = ""
            if len(msg_list) > 2 and msg_list[2] == 'g':
                result = getMemberDDL(group.id)
            else:
                result = getMemberDDL(member.id)
            await app.sendGroupMessage(group, MessageChain.create([Plain(result)]))
