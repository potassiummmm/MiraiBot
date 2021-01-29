import aiohttp
import asyncio


async def getInfoList(r_18=0) -> list:
    """
    :param r_18:
    :return list:[info/error,url/""]:
    """
    url = "https://api.lolicon.app/setu/"
    params = dict(
        apikey='592610055f91264d1a5ba8',
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
