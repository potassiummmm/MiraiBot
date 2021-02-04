from graia.application.entry import GraiaMiraiApplication, GroupMessage, MessageChain, Plain, Member, Group
import requests
from bs4 import BeautifulSoup
from core import Instance


def baidu(string: str) -> str:
    url = "http://www.baidu.com/s"

    params = dict(wd=string)

    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0",
        "Host": "www.baidu.com",
    }

    req = requests.session().get(url, params=params, headers=headers)
    soup = BeautifulSoup(req.text, 'html.parser')
    result_list = []
    result = ""
    for i in range(1, 11):
        a = soup.find(id=str(i))
        b = a.find('em')
        if b is not None:
            result_list.append(
                b.parent.text.replace('\n', '').replace(' ', ''))
    for i in range(0, len(result_list)):
        result += str(i + 1) + '.' + result_list[i] + '\n'
    return result[:-1]


bcc = Instance.bcc()


@bcc.receiver(GroupMessage)
async def group_message_listener(app: GraiaMiraiApplication, group: Group,
                                 message: MessageChain):
    if message.asDisplay().startswith("百度") and len(
            message.asDisplay().split(' ')) == 2:
        await app.sendGroupMessage(
            group,
            MessageChain.create(
                [Plain(baidu(message.asDisplay().replace(' ', '')[2:]))]))
