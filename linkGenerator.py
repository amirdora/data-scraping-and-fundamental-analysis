import os
from StockAnalysis.spiders import crawler


def generateLinksInTxt():
    for page in pages:
        link = mainUrl + page
        with open('link.txt', 'a') as the_file:
            the_file.write(link + "\n")


def removeOldFileIfExists():
    fileName = "link.txt"
    if os.path.exists(fileName):
        os.remove(fileName)


def generateLinks(ticker):
    global pages, mainUrl
    pages = crawler.pages
    ticker_arg = ticker
    mainUrl = 'https://www.macrotrends.net/stocks/charts/%s/alphabet/' % ticker_arg
    removeOldFileIfExists()
    generateLinksInTxt()
