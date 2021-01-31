import aiohttp
import asyncio
from graia.application import GraiaMiraiApplication
from graia.application.group import Group, Member
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import Image, Plain
from core import Instance
from config import SETU_API_KEY, SETU_ENABLED_GROUPS, ADMIN_QQ


async def getInfoList(r_18=0) -> list:
    """
    :param r_18:
    :return list:[info/error,url/""]:
    """
    url = "https://api.lolicon.app/setu/"
    params = dict(
        apikey=SETU_API_KEY,
        r18=r_18
    )
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, params=params) as resp:
            data_json = await resp.json()
    if data_json['code'] != 0:
        return ["涩图额度用完了", ""]
    else:
        result = """pid：%s
title: %s
author: %s
url: %s
tags: %s""" % (data_json['data'][0]['pid'], data_json['data'][0]['title'], data_json['data'][0]['author'],
               data_json['data'][0]['url'], data_json['data'][0]['tags'])
        return [result, data_json['data'][0]['url']]


bcc = Instance.bcc()


@bcc.receiver("GroupMessage")
async def group_message_listener(app: GraiaMiraiApplication, group: Group, message: MessageChain, member: Member):
    if message.asDisplay().startswith("色图"):
        if group.id in SETU_ENABLED_GROUPS:
            setu_lsit = await getInfoList(message.asDisplay().endswith("r18") + 0)
            await app.sendGroupMessage(group, MessageChain.create([Plain(setu_lsit[0])]))
            bot_message = await app.sendGroupMessage(group, MessageChain.create(
                [Image.fromNetworkAddress(url=setu_lsit[1])]))
            await asyncio.sleep(6)
            await app.revokeMessage(bot_message.messageId)
        else:
            await app.sendGroupMessage(group, MessageChain.create([Plain("别冲了")]))

    if message.asDisplay() == "可以色图" and member.id == ADMIN_QQ:
        SETU_ENABLED_GROUPS.add(group.id)
        await app.sendGroupMessage(group, MessageChain.create([Plain("开启青壮年模式")]))

    if message.asDisplay() == "禁止色图" and member.id == ADMIN_QQ:
        try:
            SETU_ENABLED_GROUPS.remove(group.id)
        except KeyError:
            pass
        await app.sendGroupMessage(group, MessageChain.create([Plain("开启青少年模式")]))

    if message.asDisplay().endswith("二次元"):
        await app.sendGroupMessage(group, MessageChain.create(
            [Image.fromNetworkAddress("https://www.fantasyzone.cc/api/tu?type=pc")]))
