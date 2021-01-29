import aiohttp
import asyncio


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
    data = dict(LanguageChoice=languageChoice, Program=code, Input=input_, CompilerArgs=compilerArgs)
    async with aiohttp.ClientSession() as session:
        async with session.post(url=api_url, data=data) as resp:
            data_json = await resp.json()
    if data_json["Errors"] is not None:
        return data_json["Errors"][:-1]
    else:
        return data_json["Result"][:-1]
