from re import S
from bs4 import BeautifulSoup
import json
import requests
import lxml.html

def steam_scrape():
    url = requests.get('https://store.steampowered.com/explore/new/')
    doc = BeautifulSoup(url.text, "lxml")
    lxmldoc = lxml.html.fromstring(url.content)
    apps = lxmldoc.xpath('//div[@id="tab_newreleases_content"]')[0]

    finalPriceList = []
    titleList = []
    tagList = []
    platformList = []
    discountList = []
    originalPriceList = []


    prices = doc.find_all("div", {"class" : [
    "discount_block tab_item_discount", 
    "discount_block tab_item_discount no_discount", 
    "discount_block empty tab_item_discount",
    ]})
    for price in prices:
        if price.text == '':
            finalPriceList.append('Free')
        else:
            pure_price = price.text
            if "%" in pure_price:
                getDiscount = pure_price.split("%")
                getOriginal = getDiscount[1].split(".")
                discountList.append(getDiscount[0])
                originalPriceList.append(getOriginal[0])
                finalPriceList.append(getOriginal[1])
            else:
                discountList.append('None')
                originalPriceList.append('None')  
                finalPriceList.append(pure_price)

    titles = doc.find_all("div", class_ = "tab_item_name")
    for title in titles:
        titleList.append(title.text)


    tags = doc.find_all("div", class_ = "tab_item_top_tags")
    for tag in tags:
        tagList.append(tag.text)

    platforms_div = apps.xpath('.//div[@class="tab_item_details"]')
    for game in platforms_div:
        temp = game.xpath('.//span[contains(@class, "platform_img")]') 
        platforms = [t.get('class').split(' ')[-1] for t in temp]
        if 'hmd_separator' in platforms:
            platforms.remove('hmd_separator')
        platformList.append(platforms)
            

    output = []
    for info in zip(titleList, finalPriceList, tagList, discountList, originalPriceList, platformList):
        resp = {}
        resp['title'] = info[0]
        resp['price'] = info[1]
        resp['discount'] = info[3]
        resp['original-price'] = info[4]
        resp['tags'] = info[2]
        resp['platform'] = info[5]
        output.append(resp)

    jsonObj = json.dumps(output)

    return(output)


print(steam_scrape())

