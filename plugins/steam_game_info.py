from graia.application.entry import GraiaMiraiApplication, Group, MessageChain, Plain
from core import Instance
from config import STEAM_API_KEY
from lxml import etree
import aiohttp


def parse(text) -> tuple:
    res = etree.HTML(text)
    try:
        return res.xpath('//*[@id="search_resultsRows"]/a[1]/@data-ds-appid')[0], res.xpath(
            '//*[@id="search_resultsRows"]/a[1]/div[2]/div[1]/span/text()')[0]
    except IndexError:
        return "", ""


async def get_name_by_id(id: str) -> str:
    url = "https://store.steampowered.com/api/appdetails?appids=" + id
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data_json = await resp.json()
            if not data_json[id]['success']:
                return ""
            else:
                return data_json[id]['data']['name']


async def get_search_info(keyword: str) -> tuple:
    url = "https://store.steampowered.com/search/?term=%s&l=schinese" % keyword
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.text()
            return parse(data)


async def get_game_plain(id: str) -> str:
    url = "https://api.isthereanydeal.com/v02/game/plain/?key=%s&shop=steam&game_id=app/%s" % (
        STEAM_API_KEY, id)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data_json = await resp.json()
            return data_json['data']['plain']


async def get_current_price_dict(plain: str) -> dict:
    url = "https://api.isthereanydeal.com/v01/game/prices/?key=%s&plains=%s&country=CN&shops=steam" % (
        STEAM_API_KEY, plain)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data_json = await resp.json()
            return data_json['data'][plain]['list'][0]


async def get_lowest_price(plain: str) -> int:
    url = "https://api.isthereanydeal.com/v01/game/lowest/?key=%s&plains=%s&country=CN&shops=steam" % (
        STEAM_API_KEY, plain)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data_json = await resp.json()
            return data_json['data'][plain]['price']


async def get_game_info(keyword: str) -> str:
    id = keyword
    name = ""
    if not str.isdigit(keyword):
        info_tuple = await get_search_info(keyword)
        id = info_tuple[0]
        name = info_tuple[1]
    else:
        name = await get_name_by_id(id)
    if id == "" or name == "":
        return "没有匹配的搜索结果"
    else:
        game_plain = await get_game_plain(id)
        current_price_dict = await get_current_price_dict(game_plain)
        lowest_price = await get_lowest_price(game_plain)
        return """游戏名:%s
原价:%d
现价:%d
折扣:-%d%%
史低:%d""" % (name, current_price_dict['price_old'], current_price_dict['price_new'],
            current_price_dict['price_cut'], lowest_price)


bcc = Instance.bcc()


@bcc.receiver("GroupMessage")
async def group_message_listener(app: GraiaMiraiApplication, group: Group, message: MessageChain):
    if message.asDisplay().startswith("steam") and len(message.asDisplay().split(' ')) > 2:
        msg = message.asDisplay()
        res = await get_game_info(msg[6:])
        await app.sendGroupMessage(group, MessageChain.create([Plain(res)]))
