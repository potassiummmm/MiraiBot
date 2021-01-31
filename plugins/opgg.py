import requests
from bs4 import BeautifulSoup
from graia.application import GraiaMiraiApplication
from graia.application.group import Group, Member
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import Plain
from core import Instance
import championName
import championInfo


def opgg(location: str):
    if location.lower() == "top" or location == "上单" or location == "上路":
        location = "TOP"
    elif location.lower() == "jungle" or location == "打野":
        location = "JUNGLE"
    elif location.lower() == "mid" or location == "中单" or location == "中路":
        location = "MID"
    elif location.lower() == "ad" or location.lower() == "adc" or location == "下路":
        location = "ADC"
    elif location.lower() == "sup" or location == "辅助":
        location = "SUPPORT"
    else:
        return "请输入正确的位置参数"

    url = "http://www.op.gg/champion/statistics"
    req = requests.session().get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    b = soup.find(class_="tabItem champion-trend-tier-" + location)
    c = b.find_all(class_="champion-index-table__name")

    result = ""

    for i in range(0, 10):
        result += str(i + 1) + '.' + c[i].next_element + '\n'
    return result[:-1]



bcc = Instance.bcc() 

@bcc.receiver("GroupMessage")
async def group_message_listener(app: GraiaMiraiApplication, group: Group, message: MessageChain, member: Member):
    if message.asDisplay().lower().startswith("lol"):
        await app.sendGroupMessage(group, MessageChain.create([Plain(opgg(message.asDisplay().replace(' ', '')[3:]))]))
        
    if message.asDisplay().endswith("符文"):
        msg = message.asDisplay().split(' ')
        await app.sendGroupMessage(group, MessageChain.create(championInfo.getChampionRunes(championName.convert(msg[0]), msg[1])))

