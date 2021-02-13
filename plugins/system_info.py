from graia.application.entry import GraiaMiraiApplication, Group, Member, MessageChain, Plain
from core import Instance
import subprocess


def getSystemInfo():
    result = subprocess.getoutput("neofetch --stdout")
    return result.strip('\n')


bcc = Instance.bcc()


@bcc.receiver("GroupMessage")
async def group_message_listener(app: GraiaMiraiApplication, group: Group,
                                 message: MessageChain, member: Member):
    if message.asDisplay() == "系统信息":
        await app.sendGroupMessage(
            group, MessageChain.create([Plain(getSystemInfo())]))
