from graia.application.entry import GraiaMiraiApplication, Group, MessageChain, Plain
from core import Instance
import requests
import json


def guess(text: str):
    url = "https://lab.magiconch.com/api/nbnhhsh/guess"
    data = {'text': text}
    r = requests.post(url, data=data)
    json_file = json.loads(r.content)
    result = text + "可能是:\n"
    try:
        results = json_file[0]['trans']
    except KeyError:
        results = json_file[0]['inputting']
    if len(results) == 0:
        result = "尚未录入"
    else:
        for i in results:
            result += i + '\n'
        result = result[:-1]
    return result


bcc = Instance.bcc()


@bcc.receiver("GroupMessage")
async def group_message_listener(app: GraiaMiraiApplication, group: Group,
                                 message: MessageChain):
    if message.asDisplay().lower().startswith("guess") and len(
            message.asDisplay().split(' ')) == 2:
        await app.sendGroupMessage(
            group,
            MessageChain.create(
                [Plain(guess(message.asDisplay().replace(' ', '')[5:]))]))
