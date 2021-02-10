from graia.application.entry import GraiaMiraiApplication, Group, Member, GroupMessage, MessageChain, Image, Plain, At
from graia.application.interrupts import GroupMessageInterrupt
from config import SETU_API_KEY, SETU_ENABLED_GROUPS, ADMIN_QQ
from core import Instance
import aiohttp
import asyncio

code_info = {
    -1: "内部错误",
    0: "成功",
    401: "APIKEY不存在或被封禁",
    403: "由于不规范的操作而被拒绝调用",
    404: "找不到符合关键字的色图",
    429: "达到调用额度限制"
}


async def getInfoList(r_18=0, keyword="") -> list:
    """
    :param r_18:
    :return list:[info/error,url/""]:
    """
    url = "https://api.lolicon.app/setu/"
    params = dict(apikey=SETU_API_KEY, r18=r_18, keyword=keyword)
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, params=params) as resp:
            data_json = await resp.json()
    if data_json['code'] != 0:
        return [code_info[data_json['code']], ""]
    else:
        result = """pid：%s
title: %s
author: %s
url: %s
tags: %s""" % (data_json['data'][0]['pid'], data_json['data'][0]['title'],
               data_json['data'][0]['author'], data_json['data'][0]['url'],
               data_json['data'][0]['tags'])
        return [result, data_json['data'][0]['url']]


bcc = Instance.bcc()
inc = Instance.inc()


@bcc.receiver("GroupMessage")
async def group_message_listener(app: GraiaMiraiApplication, group: Group,
                                 message: MessageChain, member: Member):
    if message.asDisplay().startswith("色图"):
        await app.sendGroupMessage(
            group, MessageChain.create([At(member.id),
                                        Plain("是否R18? 1 or 0")]))
        res = await inc.wait(
            GroupMessageInterrupt(
                group,
                member,
                custom_judgement=lambda x: x.messageChain.asDisplay(
                ) == "0" or x.messageChain.asDisplay() == "1"))
        command = res.messageChain.asDisplay()
        await app.sendGroupMessage(
            group, MessageChain.create([At(member.id),
                                        Plain("请输入关键词 0表示随机")]))
        res = await inc.wait(GroupMessageInterrupt(
            group,
            member,
        ))
        keyword = res.messageChain.asDisplay()
        if keyword == "0":
            keyword = ""
        if group.id in SETU_ENABLED_GROUPS:
            setu_list = await getInfoList((command == "1") + 0, keyword)
            await app.sendGroupMessage(
                group, MessageChain.create([Plain(setu_list[0])]))
            bot_message = await app.sendGroupMessage(
                group,
                MessageChain.create(
                    [Image.fromNetworkAddress(url=setu_list[1])]))
            await asyncio.sleep(6)
            await app.revokeMessage(bot_message.messageId)
        else:
            await app.sendGroupMessage(group,
                                       MessageChain.create([Plain("别冲了")]))

    if message.asDisplay() == "可以色图" and member.id == ADMIN_QQ:
        SETU_ENABLED_GROUPS.add(group.id)
        await app.sendGroupMessage(group,
                                   MessageChain.create([Plain("开启青壮年模式")]))

    if message.asDisplay() == "禁止色图" and member.id == ADMIN_QQ:
        try:
            SETU_ENABLED_GROUPS.remove(group.id)
        except KeyError:
            pass
        await app.sendGroupMessage(group,
                                   MessageChain.create([Plain("开启青少年模式")]))

    if message.asDisplay().endswith("二次元"):
        await app.sendGroupMessage(
            group,
            MessageChain.create([
                Image.fromNetworkAddress(
                    "https://www.fantasyzone.cc/api/tu?type=pc")
            ]))
