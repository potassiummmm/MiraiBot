import aiohttp
import json
import  time
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import Plain
from graia.scheduler import GraiaScheduler
from graia.scheduler.timers import every_custom_seconds
from core import Instance

async def getUserInfoJson(uuid: int) -> dict:
    url = "https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?host_uid=%d&offset_dynamic_id=0" % uuid
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data_json = await resp.json()
            return data_json


async def getLatestVideoTimestamp(uuid: int) -> int:
    data_json = await getUserInfoJson(uuid)
    return data_json["data"]["cards"][0]["desc"]["timestamp"]


async def getLatestVideoInfo(uuid: int) -> str:
    data_json = await getUserInfoJson(uuid)
    up_name = data_json["data"]["cards"][0]["desc"]["user_profile"]["info"]["uname"]
    result = "UP主%s更新了一个视频:\n" % up_name
    result += json.loads(data_json["data"]["cards"][0]["card"])["title"] + '\n'
    result += "https://www.bilibili.com/video/%s" % data_json["data"]["cards"][0]["desc"]["bvid"]
    return result


app = Instance.app()
sche = Instance.sche()

@sche.schedule(every_custom_seconds(5))
async def bilibili_subscribe_scheduler():
    ltt_newest_timestamp = await getLatestVideoTimestamp(12434430)
    van_newest_timestamp = await getLatestVideoTimestamp(23604445)
    if (time.time() - ltt_newest_timestamp < 5):
        result = await getLatestVideoInfo(12434430)
        await app.sendGroupMessage(546091207, MessageChain.create([Plain(result)]))
    if (time.time() - van_newest_timestamp < 5):
        result = await getLatestVideoInfo(23604445)
        await app.sendGroupMessage(434499605, MessageChain.create([Plain(result)]))
