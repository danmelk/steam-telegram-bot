from platform import release
from re import S
from textwrap import indent
from bs4 import BeautifulSoup
import json
import requests
import lxml.html

def steam_scrape():
    url = requests.get('https://store.steampowered.com/explore/new/')
    doc = lxml.html.fromstring(url.content)
    releases = doc.xpath('//div[@id="tab_newreleases_content"]')[0]

    titleList = []
    finalPriceList = []
    discountList = []
    originalPriceList = []
    tagList = []
    platformList = []

    game = releases.xpath('.//a[@class="tab_item app_impression_tracked"]')

    game_price = game.xpath('.//div[contains(@class, "discount_block")]')

    for price in game_price:
        print(price.text)

    titles = releases.xpath('.//div[@class="tab_item_name"]')
    for title in titles:
        print(title.text)



    platforms_div = releases.xpath('.//div[@class="tab_item_details"]')
    for game in platforms_div:
        temp = game.xpath('.//span[contains(@class, "platform_img")]') 
        platforms = [t.get('class').split(' ')[-1] for t in temp]
        if 'hmd_separator' in platforms:
            platforms.remove('hmd_separator')
        platformList.append(platforms)
            

    output = []
    for info in zip(titleList, finalPriceList, discountList, originalPriceList, tagList, platformList):
        resp = {}
        resp['title'] = info[0]
        resp['price'] = info[1]
        # resp['discount'] = info[2]
        # resp['original-price'] = info[3]
        # resp['tags'] = info[4]
        # resp['platform'] = info[5]
        # output.append(resp)

    jsonObj = json.dumps(output, indent=4)
    return(jsonObj)

print(steam_scrape())

