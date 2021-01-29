import requests
from lxml import etree


def get_newest_url():
    url = 'http://news.cyol.com/node_67071.htm'
    response = requests.get(url, verify=False)
    html = etree.HTML(response.text)
    newest_url = html.xpath(
        '/html/body/div[@class="mianbody"]/dl[@class="listMM"]/dd[@class="picB"]/ul[@class="movie-list"]/li[1]/a/@href')[
        0]

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
