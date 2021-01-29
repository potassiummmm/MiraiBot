import requests
import json


def guess(text: str):
    url = "https://lab.magiconch.com/api/nbnhhsh/guess"
    data = {'text': text}
    r = requests.post(url, data=data)
    json_file = json.loads(r.content)
    result = text + "可能是:\n"
    try:
        results = json_file[0]['trans']
    except KeyError:
        results = json_file[0]['inputting']
    if len(results) == 0:
        result = "尚未录入"
    else:
        for i in results:
            result += i + '\n'
        result = result[:-1]
    return result
