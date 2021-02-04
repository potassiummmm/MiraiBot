from graia.application.entry import GraiaMiraiApplication, Group, Member, MessageChain, Plain
import aiohttp
from core import Instance


async def run(languageChoice, code, input_=None, compilerArgs=None) -> str:
    """
    :param languageChoice: Java=4 Python=5 C(gcc)=6 C++(gcc)=7 Javascript=17 Python3=24 Node.js=23
    :param code: 代码
    :param input_: 输入
    :param compilerArgs:
    :return: 运行结果
    """
    api_url = "https://rextester.com/rundotnet/api"
    if languageChoice == 7:
        compilerArgs = "-o a.out source_file.cpp"
    data = dict(LanguageChoice=languageChoice,
                Program=code,
                Input=input_,
                CompilerArgs=compilerArgs)
    async with aiohttp.ClientSession() as session:
        async with session.post(url=api_url, data=data) as resp:
            data_json = await resp.json()
    if data_json["Errors"] is not None:
        return data_json["Errors"][:-1]
    else:
        return data_json["Result"][:-1]


bcc = Instance.bcc()


@bcc.receiver("GroupMessage")
async def code_runner(app: GraiaMiraiApplication, group: Group,
                      message: MessageChain):
    if message.asDisplay().lower().startswith("c++") and len(
            message.asDisplay()) > 4:
        result = await run(7, message.asDisplay()[4:])
        await app.sendGroupMessage(group, MessageChain.create([Plain(result)]))

    if message.asDisplay().lower().startswith("python") and len(
            message.asDisplay()) > 7:
        result = await run(24, message.asDisplay()[7:])
        await app.sendGroupMessage(group, MessageChain.create([Plain(result)]))

    if message.asDisplay().lower().startswith("java") and len(
            message.asDisplay()) > 5:
        if message.asDisplay().lower().startswith("javascript") and len(
                message.asDisplay()) > 11:
            result = await run(17, message.asDisplay()[11:])
            await app.sendGroupMessage(group,
                                       MessageChain.create([Plain(result)]))
        else:
            result = await run(4, message.asDisplay()[5:])
            await app.sendGroupMessage(group,
                                       MessageChain.create([Plain(result)]))

    if message.asDisplay().lower().startswith("nodejs") and len(
            message.asDisplay()) > 7:
        result = await run(23, message.asDisplay()[7:])
        await app.sendGroupMessage(group, MessageChain.create([Plain(result)]))
