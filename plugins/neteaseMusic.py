from graia.application.entry import GraiaMiraiApplication, Group, MessageChain, Plain
from core import Instance
import aiohttp
import json


async def get_song(keyword: str) -> str:
    search_url = "http://music.163.com/api/search/get/web?csrf_token=hlpretag=&hlposttag=&type=1&offset=0&total=true&limit=1&s=" + keyword
    async with aiohttp.ClientSession() as session:
        async with session.get(url=search_url) as resp:
            data_json = await resp.read()

    data_json = json.loads(data_json)
    try:
        result = data_json["result"]["songs"][0]["name"] + ':\n'
        song_id = data_json["result"]["songs"][0]["id"]
        song_url = "https://y.music.163.com/m/song/%s" % song_id
        play_url = "http://music.163.com/song/media/outer/url?id=%d" % song_id
        result += "歌曲链接: %s\n播放链接: %s" % (song_url, play_url)
        return result
    except KeyError:
        return "未找到歌曲信息"


async def get_comment() -> str:
    api_url = "https://nd.2890.ltd/api?format=text"
    async with aiohttp.ClientSession() as session:
        async with session.get(url=api_url) as resp:
            data = await resp.text()
    return data


bcc = Instance.bcc()


@bcc.receiver("GroupMessage")
async def group_message_listener(app: GraiaMiraiApplication, group: Group, message: MessageChain):
    if message.asDisplay().startswith("点歌"):
        result = await get_song(message.asDisplay().replace(' ', '')[2:])
        await app.sendGroupMessage(group, MessageChain.create([Plain(result)]))
