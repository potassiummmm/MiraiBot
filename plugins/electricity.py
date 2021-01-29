import asyncio
import aiohttp
import xml.dom.minidom as dom
import re


def getForm(text):
    tree = dom.parseString(text)
    form = {}
    inputs = tree.getElementsByTagName('input')
    for i in inputs:
        name, value = i.getAttribute('name'), i.getAttribute('value')
        form[name] = value
    return form


url = 'http://202.120.163.129:88'


async def updateForm(session, form, **data):
    form.update(data)
    async with session.post(url, data=form) as resp:
        text = await resp.text()
    form.update(getForm(text))
    # print(form)
    # print(text)


async def main(data):
    async with aiohttp.ClientSession() as s:
        async with s.get(url) as resp:
            text = await resp.text()
        # print(text)
        form = getForm(text)
        
        for k,v in data.items():
          await updateForm(s, form, **{k:v})
        
        form.update({
            'radio': 'usedR',
            'ImageButton1.x': 51,
            'ImageButton1.y': 37})
        # print(form)
        async with s.post(url, data=form, allow_redirects=False) as resp:
            # print(await resp.text())
            # print(resp.cookies)
            c = resp.cookies # nm怎么Set-Cookie用不了

        async with s.get(url+'/usedRecord1.aspx', cookies=c) as resp:
            text = await resp.text()
            # print(text)
            return float(re.findall(r'剩余电量.+?(\d+\.?\d*)', text)[0])

data = {
    'drlouming': '9',
    'drceng': '20',
    'dr_ceng': '2005',
    'drfangjian': '200512',
}
print(asyncio.run(main(data)))
