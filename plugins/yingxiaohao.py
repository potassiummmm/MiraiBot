from graia.application import GraiaMiraiApplication
from graia.application.group import Group, Member
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import Plain
from core import Instance


def getText(keyword1: str, keyword2: str, keyword3: str):
    return "kw1kw2?看到专家回复，网友直呼安心。\n近日，kw1kw2，引发了众人的关注。" \
           "众所周知，kw1kw2，那么kw1kw2又是怎么一回事呢？真可谓是大千世界无奇不有，" \
           "让我们和小编一起来看看吧。\nkw1相信大家都很熟悉，kw1kw2就是我们每天都会经常遇到的。" \
           "随着人们生活水平的提高和科技的进步，kw1kw2也被越来越多人所知。但是kw1kw2是怎么回事呢，" \
           "下面就让小编带大家一起了解吧。\nkw1kw2，其实就是kw3。kw1kw2最近能火，" \
           "其实就是kw3受到了大家的关注。大家可能会很惊讶kw1怎么会kw2呢？但事实就是这样，" \
           "小编也感到非常惊讶。\nkw1到底有多会kw2，小编是真的不知道。对kw1，小编也只是久仰过大名却从不见真身。\n" \
           "这就是关于kw1kw2的事情了，大家有什么想法呢，" \
           "欢迎在评论区告诉小编一起讨论哦！".replace("kw1", keyword1).replace("kw2", keyword2).replace("kw3", keyword3)


bcc = Instance.bcc() 

@bcc.receiver("GroupMessage")
async def group_message_listener(app: GraiaMiraiApplication, group: Group, message: MessageChain, member: Member):
    if message.asDisplay().startswith("营销号"):
        msg = message.asDisplay().split(' ')
        await app.sendGroupMessage(group, MessageChain.create([Plain(getText(msg[1], msg[2], msg[3]))]))

