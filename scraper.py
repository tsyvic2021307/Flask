import requests
from bs4 import BeautifulSoup
from statistics import mean
from decimal import Decimal
TWOPLACES = Decimal(10) ** -2


def scrape(link):
    fulllist = []
    pagenumber = 1
    done = False
    while not done:
        response = requests.get("%s?buy=buynow&page=%d" %(link, pagenumber))
        pagenumber += 1 
        soup = BeautifulSoup(response.text, "html.parser")
        totalcount = int(soup.find("span", {"id":"totalCount"}).text.strip())
        lowcount = int(soup.find("span", {"id":"lowCount"}).text.strip())
        if totalcount < lowcount:
            done = True
        else:
            itemlist = soup.findAll("a")
            fulllist += itemlist
    return fulllist           


def process(fulllist):
    goodlist = []
    for item in fulllist:
        try:
            item_title = item.find("div", {"class":"title"}).text.strip()
            item_price = item.find("div", {"class":"listingBuyNowPrice"}).text.strip()
        except:
            continue
        item_URL = "https://trademe.co.nz" + item["href"]
        # print(item_title, item_price, item_URL)
        for item in goodlist:
            if item["title"] == item_title and item["price"] == item_price:
                break
        else:
            goodlist.append({"title" : item_title, "price" : item_price, "url" : item_URL})
    return goodlist

def stripMoney(val):
    price = Decimal(val.lstrip("$")).quantize(TWOPLACES)
    return price

def priceProcess(theList):
    mini = stripMoney(theList[0]["price"])
    maxi = stripMoney(theList[0]["price"])
    ave = 0
    prices = []
    for item in theList:
        price = stripMoney(item["price"])
        if price < mini:
            mini = price
        if price > maxi:
            maxi = price
        prices.append(price)
    ave = mean(prices).quantize(TWOPLACES)
    return mini, maxi, ave




