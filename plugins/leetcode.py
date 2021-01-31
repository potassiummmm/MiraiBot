import re
import requests
import json
import asyncio
from html import unescape
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import Plain
from graia.scheduler import crontabify
from core import Instance


def htmlToPlainText(html) -> str:
    text = re.sub('<head.*?>.*?</head>', '', html, flags=re.M | re.S | re.I)
    text = re.sub('<a\s.*?>', ' HYPERLINK ', text, flags=re.M | re.S | re.I)
    text = re.sub('<.*?>', '', text, flags=re.M | re.S)
    text = re.sub(r'(\s*\n)+', '\n', text, flags=re.M | re.S)
    return unescape(text)


# 含有img标签的html格式转纯文字
def imageInHtmlToText(content):
    images = re.findall(r'<img.*?src="(.*?)".*?>', content, re.S)
    for i in range(len(images)):
        content = content.replace(images[i], "/>ImAgEiMaGe%dImAgE<img" % i)
    transformed = htmlToPlainText(content)
    transformed = transformed.split("ImAgE")
    return (transformed, images)


def getQuestionContent(questionTitleSlug, language):
    url = "https://leetcode-cn.com/graphql/"
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "content-type": "application/json",
        "origin": "https://leetcode-cn.com",
        "referer": "https://leetcode-cn.com/problems/%s/" % questionTitleSlug,
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36",
        "x-definition-name": "question",
        "x-operation-name": "questionData",
        "x-timezone": "Asia/Shanghai"
    }
    payload = {
        "operationName": "questionData",
        "variables": {"titleSlug": "%s" % questionTitleSlug},
        "query": "query questionData($titleSlug: String!) {\n  question(titleSlug: $titleSlug) {\n    questionId\n    questionFrontendId\n    boundTopicId\n    title\n    titleSlug\n    content\n    translatedTitle\n    translatedContent\n    isPaidOnly\n    difficulty\n    likes\n    dislikes\n    isLiked\n    similarQuestions\n    contributors {\n      username\n      profileUrl\n      avatarUrl\n      __typename\n    }\n    langToValidPlayground\n    topicTags {\n      name\n      slug\n      translatedName\n      __typename\n    }\n    companyTagStats\n    codeSnippets {\n      lang\n      langSlug\n      code\n      __typename\n    }\n    stats\n    hints\n    solution {\n      id\n      canSeeDetail\n      __typename\n    }\n    status\n    sampleTestCase\n    metaData\n    judgerAvailable\n    judgeType\n    mysqlSchemas\n    enableRunCode\n    envInfo\n    book {\n      id\n      bookName\n      pressName\n      source\n      shortDescription\n      fullDescription\n      bookImgUrl\n      pressImgUrl\n      productUrl\n      __typename\n    }\n    isSubscribed\n    isDailyQuestion\n    dailyRecordStatus\n    editorType\n    ugcQuestionId\n    style\n    __typename\n  }\n}\n"
    }
    dataJson = requests.post(url=url, headers=headers, data=json.dumps(payload)).json()
    if language == "En":
        return dataJson["data"]["question"]["content"]
    elif language == "Zh":
        return dataJson["data"]["question"]["translatedContent"]
    else:
        return None


def getDailyQuestionJson():
    url = "https://leetcode-cn.com/graphql/"
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "content-length": "302",
        "content-type": "application/json",
        "origin": "https://leetcode-cn.com",
        "referer": "https://leetcode-cn.com/problemset/all/",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"
    }
    payload = {
        "operationName": "questionOfToday",
        "variables": {},
        "query": "query questionOfToday {\n  todayRecord {\n    question {\n      questionFrontendId,\n      questionTitleSlug,\n      __typename\n    }\n    lastSubmission {\n      id,\n      __typename,\n    }\n    date,\n    userStatus,\n    __typename\n  }\n}\n"
    }
    dataJson = requests.post(url=url, headers=headers, data=json.dumps(payload)).json()
    return dataJson


def getDailyQuestion():
    dailyQuestionData = getDailyQuestionJson()
    questionTitleSlug = dailyQuestionData["data"]["todayRecord"][0]["question"]["questionTitleSlug"]
    content = getQuestionContent(questionTitleSlug, "Zh")
    return htmlToPlainText(content)[:-1]

sche = Instance.sche()
app = Instance.app()

@sche.schedule(crontabify("0 0 * * *"))
async def leetcode_everyday_question_scheduler():
    await asyncio.sleep(1)
    await app.sendGroupMessage(1067920415, MessageChain.create([Plain(getDailyQuestion())]))

