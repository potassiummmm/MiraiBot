from graia.application.entry import GraiaMiraiApplication, GroupMessage, MessageChain, Plain, Group
from graia.scheduler.timers import every_custom_seconds
from config import BILIBILI_SUBSCRIBE_SETTINGS
import aiohttp
import json
import time
from core import Instance


async def getUserInfoJson(uuid: int) -> dict:
    url = "https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?host_uid=%d&offset_dynamic_id=0" % uuid
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data_json = await resp.json()
            return data_json


async def judgeUuid(uuid: int) -> tuple:
    url = "https://api.bilibili.com/x/space/acc/info?mid=%d" % uuid
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data_json = await resp.json()
            return (True,
                    data_json["data"]["name"]) if data_json["code"] == 0 else (
                        False, data_json["message"])


async def getLatestVideoTimestamp(uuid: int) -> int:
    data_json = await getUserInfoJson(uuid)
    return data_json["data"]["cards"][0]["desc"]["timestamp"]


async def getLatestVideoInfo(uuid: int) -> str:
    data_json = await getUserInfoJson(uuid)
    up_name = data_json["data"]["cards"][0]["desc"]["user_profile"]["info"][
        "uname"]
    result = "UP主%s更新了一个视频:\n" % up_name
    result += json.loads(data_json["data"]["cards"][0]["card"])["title"] + '\n'
    result += "https://www.bilibili.com/video/%s" % data_json["data"]["cards"][
        0]["desc"]["bvid"]
    return result


app = Instance.app()
sche = Instance.sche()
bcc = Instance.bcc()


@sche.schedule(every_custom_seconds(5))
async def bilibili_subscribe_scheduler():
    for group in BILIBILI_SUBSCRIBE_SETTINGS:
        for up in BILIBILI_SUBSCRIBE_SETTINGS[group]:
            latest_timestamp = await getLatestVideoTimestamp(up)
            if time.time() - latest_timestamp < 5:
                result = await getLatestVideoInfo(up)
                await app.sendGroupMessage(
                    group, MessageChain.create([Plain(result)]))


@bcc.receiver("GroupMessage")
async def bilibili_subscribe_auth_listener(app: GraiaMiraiApplication,
                                           group: Group,
                                           message: MessageChain):
    if message.asDisplay().startswith("订阅") and len(
            message.asDisplay().split(' ')) == 2:
        try:
            uuid = int(message.asDisplay().split(' ')[1])
            res = await judgeUuid(uuid)
            msg = MessageChain.create([Plain(res[1])])
            if res[0]:  # 请求成功
                print("请求成功")
                if (uuid in BILIBILI_SUBSCRIBE_SETTINGS[group.id]):
                    msg.plus(MessageChain.create([Plain("已订阅 请勿重复操作")]))
                else:
                    BILIBILI_SUBSCRIBE_SETTINGS[group.id].add(uuid)
                    msg.plus(MessageChain.create([Plain(" 订阅成功!")]))
            await app.sendGroupMessage(group, msg)
        except ValueError:
            msg = MessageChain.create(Plain("请输入整数uuid"))
            await app.sendGroupMessage(group, msg)

    if message.asDisplay().startswith("取消订阅") and len(
            message.asDisplay().split(' ')) == 2:
        try:
            uuid = int(message.asDisplay().split(' ')[1])
            res = await judgeUuid(uuid)
            msg = MessageChain.create([Plain(res[1])])
            if res[0]:  # 请求成功
                if (uuid in BILIBILI_SUBSCRIBE_SETTINGS[group.id]):
                    BILIBILI_SUBSCRIBE_SETTINGS[group.id].remove(uuid)
                    msg.plus(MessageChain.create([Plain(" 取消订阅成功!")]))
                else:
                    msg.plus(MessageChain.create([Plain("未订阅 无法取消")]))
            await app.sendGroupMessage(group, msg)
        except ValueError:
            msg = MessageChain.create(Plain("请输入整数uuid"))
            await app.sendGroupMessage(group, msg)

    if message.asDisplay() == "订阅列表":
        content = "订阅列表:"
        if len(BILIBILI_SUBSCRIBE_SETTINGS[group.id]) == 0:
            content = "订阅列表为空"
        else:
            for up in BILIBILI_SUBSCRIBE_SETTINGS[group.id]:
                res = await judgeUuid(up)
                content = content.join("\n").join(res[1])
        await app.sendGroupMessage(group,
                                   MessageChain.create([Plain(content)]))
