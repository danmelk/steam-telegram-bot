from bs4 import BeautifulSoup
import json
import requests
import lxml.html

def steam_scrape():
    url = requests.get('https://store.steampowered.com/search/?filter=popularnew&sort_by=Released_DESC')
    doc = BeautifulSoup(url.text, "lxml")
    lxmldoc = lxml.html.fromstring(url.content)
    apps = lxmldoc.xpath('//div[@id="search_resultsRows"]')[0]

    currentPriceList = []
    titleList = []
    platformList = []
    discountList = []
    originalPriceList = []
    dateList = []
    reviewList = []


    titles = doc.find_all("span", class_ = "title")
    for title in titles:
        titleList.append(title.text)

    discountPrices = doc.find_all("div", {"class" : [
    "col search_price discounted responsive_secondrow", 
    "col search_price responsive_secondrow",
    ]})
    for price in discountPrices:
        fixed = " ".join(price.text.split())
        currentPrice = fixed.split('.') #€
        if len(currentPrice) == 3:
            originalPriceList.append(currentPrice[0])
            currentPriceList.append(currentPrice[1])
        else:
            currentPriceList.append(currentPrice[0])
            originalPriceList.append('None')

    discounts = doc.find_all("div", class_ = 'col search_discount responsive_secondrow')
    for discount in discounts:
        fixed = " ".join(discount.text.split())
        if fixed == '':
            discountList.append('None')
        else:
            discountList.append(fixed)

    platforms_div = apps.xpath('.//div[@class="col search_name ellipsis"]')
    for game in platforms_div:
        temp = game.xpath('.//span[contains(@class, "platform_img")]') 
        platforms = [t.get('class').split(' ')[-1] for t in temp]
        if 'hmd_separator' in platforms:
            platforms.remove('hmd_separator')
        platformList.append(platforms)

    date = doc.find_all("div", class_ = 'col search_released responsive_secondrow')
    for entry in date:
        dateList.append(entry.text)
            
    for feedback in doc.find_all('span', {'data-tooltip-html' : True}):
        review = feedback['data-tooltip-html'].split("<br>")
        reviewList.append(review)

    output = []
    for info in zip(titleList, currentPriceList, discountList, originalPriceList, platformList, dateList, reviewList):
        resp = {}
        resp['title'] = info[0]
        resp['price'] = info[1]
        resp['discount'] = info[2]
        resp['original-price'] = info[3]
        resp['platform'] = info[4]
        resp['date'] = info[5]
        resp['review'] = info[6]
        output.append(resp)

    return(output)

steam_scrape()

