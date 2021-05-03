from graia.application.entry import GraiaMiraiApplication, Group, MessageChain, Plain
from core import Instance
import random


def get_yxh_text(keyword1: str, keyword2: str, keyword3: str):
    return "kw1kw2?看到专家回复，网友直呼安心。\n近日，kw1kw2，引发了众人的关注。" \
           "众所周知，kw1kw2，那么kw1kw2又是怎么一回事呢？真可谓是大千世界无奇不有，" \
           "让我们和小编一起来看看吧。\nkw1相信大家都很熟悉，kw1kw2就是我们每天都会经常遇到的。" \
           "随着人们生活水平的提高和科技的进步，kw1kw2也被越来越多人所知。但是kw1kw2是怎么回事呢，" \
           "下面就让小编带大家一起了解吧。\nkw1kw2，其实就是kw3。kw1kw2最近能火，" \
           "其实就是kw3受到了大家的关注。大家可能会很惊讶kw1怎么会kw2呢？但事实就是这样，" \
           "小编也感到非常惊讶。\nkw1到底有多会kw2，小编是真的不知道。对kw1，小编也只是久仰过大名却从不见真身。\n" \
           "这就是关于kw1kw2的事情了，大家有什么想法呢，" \
           "欢迎在评论区告诉小编一起讨论哦！".replace("kw1", keyword1).replace("kw2", keyword2).replace("kw3", keyword3)


def get_riddler_text():
    content_list = [
        "关于这个事，我简单说两句，至于我的身份，你明白就行。", "总而言之，这个事呢，现在就是这个情况，具体的呢，大家也都看得到。", "我因为这个身份上的问题，也得出来说那么几句。",
        "可能，你听的不是很明白，但是意思就是那么个意思。", "我的身份呢，不知道的你也不用去猜,这种事情见得多了，我只想说懂得都懂，不懂的我也不多解释，毕竟自己知道就好。",
        "细细品吧。你们也别来问我怎么了，利益牵扯太大，说了对你我都没好处，当不知道就行了，其余的我只能说这里面水很深，牵扯到很多东西。",
        "详细情况你们自己是很难找的，网上大部分已经删除干净了，所以我只能说懂得都懂。",
        "懂的人已经基本都获利上岸什么的了，不懂的人永远不懂，关键懂的人都是自己悟的，你也不知道谁是懂的人也没法请教，大家都藏着掖着生怕别人知道自己懂事。",
        "懂了就能收割不懂的，你甚至都不知道自己不懂。只是在有些时候，某些人对某些事情不懂装懂，还以为别人不懂。", "其实自己才是不懂的，别人懂的够多了，不仅懂，还懂的超越了这个范围。",
        "但是某些不懂的人让这个懂的人完全教不懂，所以不懂的人永远不懂，只能不懂装懂。",
        "别人说懂的都懂，只要点点头就行了，其实你懂的我也懂,谁让我们都懂呢,不懂的话也没必要装懂,毕竟里面牵扣扯到很多懂不了的事。",
        "这种事懂的人也没必要访出来,不懂的人看见又来问七问八,最后跟他说了他也不一定能懂,就算懂了以后也对他不好,毕竟懂的太多了不是好事。",
        "所以大家最好是不懂就不要去了解,懂太多不好。"
    ]
    random_seq = random.sample(range(len(content_list)), 3)
    return content_list[random_seq[0]] + content_list[random_seq[1]] + content_list[random_seq[2]]


bcc = Instance.bcc()


@bcc.receiver("GroupMessage")
async def group_message_listener(app: GraiaMiraiApplication, group: Group, message: MessageChain):
    if message.asDisplay().startswith("营销号"):
        msg = message.asDisplay().split(' ')
        await app.sendGroupMessage(
            group, MessageChain.create([Plain(get_yxh_text(msg[1], msg[2], msg[3]))]))
    if message.asDisplay().startswith("谜语人") or message.asDisplay().startswith("猜谜"):
        await app.sendGroupMessage(group, MessageChain.create([Plain(get_riddler_text())]))
