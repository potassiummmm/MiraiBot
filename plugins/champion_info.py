from graia.application.message.elements.internal import Image
import requests
from bs4 import BeautifulSoup
import re
from io import BytesIO
from PIL import Image as Img


def getChampionRunes(championName: str, location: str):
    if location.lower() == "top" or location == "上单" or location == "上路":
        location = "top"
    elif location.lower() == "jungle" or location == "打野":
        location = "jungle"
    elif location.lower() == "mid" or location == "中单" or location == "中路":
        location = "mid"
    elif location.lower() == "ad" or location.lower() == "adc" or location == "下路":
        location = "adc"
    elif location.lower() == "sup" or location == "辅助":
        location = "support"
    else:
        location = "top"
    url = "http://www.op.gg/champion/" + championName + "/statistics/" + location
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    a = soup.find_all("div", {"class": re.compile("perk-page__item--active$")})
    runeUrls = []
    for b in a:
        runeUrls.append("http:" + b.find("img")["src"])
    result = []
    for url in runeUrls[0:6]:
        r = requests.get(url, stream=True)
        image = Img.open(BytesIO(r.content))
        image = image.resize((32, 32))
        newImgByteArr = BytesIO()
        image.save(newImgByteArr, format='PNG')
        result.append(Image.fromUnsafeBytes(newImgByteArr.getvalue()))
    return result
