from graia.application.entry import GraiaMiraiApplication, Group, MessageChain, Plain
from core import Instance
import requests
import json


def search(repositoryName: str):
    url = "https://api.github.com/search/repositories?q=" + repositoryName
    r = requests.get(url)
    json_file = json.loads(r.content)
    data = json_file["items"][0]
    result = """%s
Owner: %s
Description: %s
Watch / Star / Fork: %d / %d / %d
Language: %s
License: %s
Last updated: %s
Jump: %s""" % (data["full_name"], data["owner"]["login"], data["description"],
               data["watchers_count"], data["stargazers_count"], data["forks_count"],
               data["language"], data["license"] if data["license"] is None else
               data["license"]["spdx_id"], data["updated_at"], data["html_url"])
    return result


bcc = Instance.bcc()


@bcc.receiver("GroupMessage")
async def group_message_listener(app: GraiaMiraiApplication, group: Group, message: MessageChain):
    if message.asDisplay().lower().startswith("github") and len(
            message.asDisplay().split(' ')) == 2:
        await app.sendGroupMessage(
            group, MessageChain.create([Plain(search(message.asDisplay().replace(' ', '')[6:]))]))
