import requests
import json
from graia.application import GraiaMiraiApplication
from graia.application.group import Group, Member
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import Plain
from core import Instance


def getPoetry():
    url = "https://v1.jinrishici.com/all.json"
    response = requests.get(url)
    json_file = json.loads(response.content)
    return json_file["content"]


print(getPoetry())

bcc = Instance.bcc()


@bcc.receiver("GroupMessage")
async def group_message_listener(app: GraiaMiraiApplication, group: Group, message: MessageChain, member: Member):
    if message.asDisplay() == "念诗" or message.asDisplay() == "诗词":
        await app.sendGroupMessage(group, MessageChain.create([Plain(getPoetry())]))
