from graia.application.entry import GraiaMiraiApplication, Group, MessageChain, Plain
from graia.scheduler.timers import crontabify
from core import Instance
from config import LEETCODE_ENABLED_GROUPS
import requests
import json
import asyncio
from bs4 import BeautifulSoup


def get_daily_question():
    base_url = 'https://leetcode-cn.com'

    response = requests.post(
        base_url + "/graphql",
        json={
            "operationName":
            "questionOfToday",
            "variables": {},
            "query":
            "query questionOfToday { todayRecord {   question {     questionFrontendId     questionTitleSlug     __typename   }   lastSubmission {     id     __typename   }   date   userStatus   __typename }}"
        })
    leetcodeTitle = json.loads(
        response.text).get('data').get('todayRecord')[0].get("question").get('questionTitleSlug')

    url = base_url + "/problems/" + leetcodeTitle
    response = requests.post(
        base_url + "/graphql",
        json={
            "operationName":
            "questionData",
            "variables": {
                "titleSlug": leetcodeTitle
            },
            "query":
            "query questionData($titleSlug: String!) {  question(titleSlug: $titleSlug) {    questionId    questionFrontendId    boundTopicId    title    titleSlug    content    translatedTitle    translatedContent    isPaidOnly    difficulty    likes    dislikes    isLiked    similarQuestions    contributors {      username      profileUrl      avatarUrl      __typename    }    langToValidPlayground    topicTags {      name      slug      translatedName      __typename    }    companyTagStats    codeSnippets {      lang      langSlug      code      __typename    }    stats    hints    solution {      id      canSeeDetail      __typename    }    status    sampleTestCase    metaData    judgerAvailable    judgeType    mysqlSchemas    enableRunCode    envInfo    book {      id      bookName      pressName      source      shortDescription      fullDescription      bookImgUrl      pressImgUrl      productUrl      __typename    }    isSubscribed    isDailyQuestion    dailyRecordStatus    editorType    ugcQuestionId    style    __typename  }}"
        })
    jsonText = json.loads(response.text).get('data').get("question")

    no = jsonText.get('questionFrontendId')
    leetcodeTitle = jsonText.get('translatedTitle')
    context = jsonText.get('translatedContent')
    context = BeautifulSoup(context, 'html.parser').get_text()
    result = f"{no}.{leetcodeTitle}\n{context}\n{url}"
    return result


sche = Instance.sche()
app = Instance.app()
bcc = Instance.bcc()


@sche.schedule(crontabify("0 0 * * *"))
async def leetcode_everyday_question_scheduler():
    await asyncio.sleep(1)
    result = get_daily_question()
    for group in LEETCODE_ENABLED_GROUPS:
        await app.sendGroupMessage(group, MessageChain.create([Plain(result)]))


@bcc.receiver("GroupMessage")
async def leetcode_auth_listener(app: GraiaMiraiApplication, group: Group, message: MessageChain):
    if message.asDisplay().lower() == "leetcode on":
        LEETCODE_ENABLED_GROUPS.add(group.id)
        await app.sendGroupMessage(group, MessageChain.create([Plain("已开启LeetCode每日一题推送")]))
    elif message.asDisplay().lower() == "leetcode off":
        try:
            LEETCODE_ENABLED_GROUPS.remove(group.id)
            await app.sendGroupMessage(group, MessageChain.create([Plain("已关闭LeetCode每日一题推送")]))
        except KeyError as e:
            await app.sendGroupMessage(group, MessageChain.create([Plain("本群未开启LeetCode每日一题推送!")]))
            print(e)
