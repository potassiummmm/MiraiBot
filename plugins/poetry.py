import requests
import json


def getPoetry():
    url = "https://v1.jinrishici.com/all.json"
    response = requests.get(url)
    json_file = json.loads(response.content)
    return json_file["content"]


print(getPoetry())

