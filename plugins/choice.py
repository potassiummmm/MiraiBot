from graia.application.entry import GraiaMiraiApplication, Group, MessageChain, Plain
import random
import datetime
from core import Instance


def makeChoice(*paras):
    random.seed(datetime.datetime.now())
    return paras[random.randint(0, len(paras) - 1)]


bcc = Instance.bcc()


@bcc.receiver("GroupMessage")
async def group_message_listener(app: GraiaMiraiApplication, group: Group,
                                 message: MessageChain):
    if message.asDisplay().startswith("选择"):
        if message.asDisplay().find(' ') == -1:
            await app.sendGroupMessage(
                group, MessageChain.create([Plain("请输入空格分割的选项")]))
        else:
            msg = message.split(' ')
            await app.sendGroupMessage(group, makeChoice(*msg[1:]))
