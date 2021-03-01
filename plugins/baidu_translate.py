from graia.application.entry import GraiaMiraiApplication, GroupMessage, MessageChain, Plain, Group
from hashlib import md5
from config import BAIDU_TRANSLATE_APP_ID, BAIDU_TRANSLATE_SECRET_KEY
from core import Instance
import aiohttp

app = Instance.app()
bcc = Instance.bcc()


@bcc.receiver("GroupMessage")
async def baidu_translator_listener(app: GraiaMiraiApplication, group: Group,
                                    message: MessageChain):
    if message.asDisplay().startswith("translate") and len(
            message.asDisplay().split(' ')) == 2:
        query = message.asDisplay().split(' ')[1]
        res = BAIDU_TRANSLATE_APP_ID + query + "1926" + BAIDU_TRANSLATE_SECRET_KEY
        sign = md5(res.encode('utf8')).hexdigest()
        url = "http://api.fanyi.baidu.com/api/trans/vip/translate?q=%s&from=auto&to=zh&appid=%s&salt=1926&sign=%s" % (
            query, BAIDU_TRANSLATE_APP_ID, sign)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                data_json = await resp.json()
                await app.sendGroupMessage(
                    group,
                    MessageChain.create(
                        [Plain(data_json["trans_result"][0]["dst"])]))
