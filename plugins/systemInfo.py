import subprocess
from graia.application import GraiaMiraiApplication
from graia.application.group import Group, Member
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import Plain
from core import Instance


def getSystemInfo():
    result = subprocess.getoutput("neofetch --stdout")
    return result.strip('\n')

bcc = Instance.bcc() 

@bcc.receiver("GroupMessage")
async def group_message_listener(app: GraiaMiraiApplication, group: Group, message: MessageChain, member: Member):
    if message.asDisplay() == "系统信息":
        await app.sendGroupMessage(group, MessageChain.create([Plain(getSystemInfo())]))
