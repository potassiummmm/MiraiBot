import aiohttp
from graia.application import GraiaMiraiApplication
from graia.application.message.chain import MessageChain
from graia.application.event.messages import Group, Member
from graia.application.message.elements.internal import Plain, At, Image
from graia.application.interrupts import GroupMessageInterrupt
from core import Instance
from config import SAUCENAO_COOKIE


async def search_image(img: Image) -> MessageChain:
    url = "https://saucenao.com/search.php"
    pic_url = img.url
    print(pic_url)
    payload = {
        "url": pic_url,
        "numres": 1,
        "testmode": 1,
        "db": 999,
        "output_type": 2,
    }
    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Referer": url,
        "Origin": "https://saucenao.com",
        "Host": "saucenao.com",
        "cookie": SAUCENAO_COOKIE
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url=url, headers=headers, data=payload) as resp:
            json_data = await resp.json()

    if json_data["header"]["status"] == -1:
        return MessageChain.create([Plain(text=f"错误：{json_data['header']['message']}")])

    if not json_data["results"]:
        return MessageChain.create([Plain(text="没有搜索到结果")])

    result = json_data["results"][0]
    header = result["header"]
    data = result["data"]

    async with aiohttp.ClientSession() as session:
        async with session.get(url=header["thumbnail"]) as resp:
            img_content = await resp.read()

    similarity = header["similarity"]
    data_str = f"搜索到如下结果：\n相似度：{similarity}%"
    for key in data.keys():
        if isinstance(data[key], list):
            data_str += (f"\n{key}:\n" + "\n".join(data[key]))
        else:
            data_str += f"\n{key}:\n{data[key]}"
    return MessageChain.create([Image.fromUnsafeBytes(img_content), Plain(text=f"\n{data_str}")])


bcc = Instance.bcc()
inc = Instance.inc()


@bcc.receiver("GroupMessage")
async def group_message_listener(app: GraiaMiraiApplication, group: Group, message: MessageChain,
                                 member: Member):
    if message.asDisplay().startswith("搜图"):
        await app.sendGroupMessage(group, MessageChain.create([At(member.id), Plain("请发送要搜索的图片")]))
        res = await inc.wait(
            GroupMessageInterrupt(group,
                                  member,
                                  custom_judgement=lambda x: x.messageChain.has(Image)))
        img = res.messageChain.get(Image)[0]
        await app.sendGroupMessage(group, await search_image(img))
