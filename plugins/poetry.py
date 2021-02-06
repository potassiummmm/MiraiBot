from graia.application.entry import GraiaMiraiApplication, Group, Member, MessageChain, Plain
from core import Instance
import requests
import json


def getPoetry():
    url = "https://v1.jinrishici.com/all.json"
    response = requests.get(url)
    json_file = json.loads(response.content)
    return json_file["content"]


bcc = Instance.bcc()


@bcc.receiver("GroupMessage")
async def group_message_listener(app: GraiaMiraiApplication, group: Group,
                                 message: MessageChain, member: Member):
    if message.asDisplay() == "念诗" or message.asDisplay() == "诗词":
        await app.sendGroupMessage(group,
                                   MessageChain.create([Plain(getPoetry())]))
