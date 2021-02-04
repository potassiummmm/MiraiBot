from graia.application.entry import MessageChain, Plain
from graia.scheduler.timers import every_custom_minutes
import requests
from lxml import etree
from core import Instance


def get_newest_url():
    url = 'http://news.cyol.com/node_67071.htm'
    response = requests.get(url, verify=False)
    html = etree.HTML(response.text)
    newest_url = html.xpath(
        '/html/body/div[@class="mianbody"]/dl[@class="listMM"]/dd[@class="picB"]/ul[@class="movie-list"]/li[1]/a/@href'
    )[0]

    return newest_url


# 获取最新一期标题
def get_title_text():
    url = get_newest_url()
    response = requests.get(url, verify=False)
    response.encoding = 'utf-8'
    html = etree.HTML(response.text)
    title = html.xpath('/html/head/title/text()')[0]

    return title


def get_formatted_result():
    result = get_title_text() + "开始啦!还不学的都是懒狗\n" + get_newest_url()
    return result


app = Instance.app()
sche = Instance.sche()

daxuexi_newest_title = get_title_text()


@sche.schedule(every_custom_minutes(10))
async def daxuexi_scheduler():
    global daxuexi_newest_title
    if daxuexi_newest_title != get_title_text():
        result = get_formatted_result()
        daxuexi_newest_title = get_title_text
        group_list = {855840079, 434499605, 546091207}
        for i in group_list:
            await app.sendGroupMessage(i, MessageChain.create([Plain(result)]))
