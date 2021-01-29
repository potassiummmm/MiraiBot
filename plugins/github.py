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
Jump: %s""" % (
        data["full_name"], data["owner"]["login"], data["description"], data["watchers_count"],
        data["stargazers_count"],
        data["forks_count"], data["language"],
        data["license"] if data["license"] is None else data["license"]["spdx_id"],
        data["updated_at"], data["html_url"])
    return result
