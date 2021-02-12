from graia.application.entry import GraiaMiraiApplication, GroupMessage, MessageChain, Plain, Group, Member
from core import Instance

help_text = """0  百度+关键词 返回百度搜索结果
1  哔哩哔哩 订阅UP主实时推送更新
2  lol 从op.gg查询英雄数据
3  选择+选项 随机选择
4  语言+代码 对应语言运行代码
5  青年大学习 推送青年大学习栏目
6  GitHub+仓库名 查询GitHub仓库信息
7  guess+缩写 查询缩写含义(nbnhhsh)
8  leetcode 推送leetcode每日一题
9  点歌+歌曲名 网易云点歌
10 诗词/念诗 随机诗词
11 知乎热榜
13 色图
14 系统信息 查看机器运行情况
15 营销号/谜语人 关键词回复"""

bcc = Instance.bcc()


@bcc.receiver("GroupMessage")
async def help_listener(app: GraiaMiraiApplication, group: Group,
                        message: MessageChain):
    if message.asDisplay().endswith("help"):
        await app.sendGroupMessage(group,
                                   MessageChain.create([Plain(help_text)]))
