import requests
import json



def getZhihuHotLists():
    url_api = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0",
    }
    req = requests.get(url_api, headers=headers)
    result = json.loads(req.content)
    text = "知乎热榜:\n"
    for i in range(0, 9):
        text += str(i + 1) + '   ' + result["data"][i]["target"]["title"] + '\n'
    text += str(10) + '  ' + result["data"][9]["target"]["title"]
    return text
