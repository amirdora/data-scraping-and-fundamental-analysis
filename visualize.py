import json
import os

import numpy
import pandas as pd
from matplotlib import pyplot as plt


def calculatePercentage(obtained, total):
    amountInPercent = []
    for i in range(0, len(obtained)):
        amountInPercent.append(int((obtained[i] / total[i]) * 100))
    return amountInPercent


def calculateGrowth(amount):
    revenueList = [0]
    length = len(amount) - 1
    for i in range(0, length, 1):
        dividend = float(amount[i + 1]) - float(amount[i])
        divisor = float(amount[i])
        revenueList.append(int((dividend / divisor) * 100))
    return revenueList


def showPercentChart(year, percentage, title, description):
    plt.plot(year, percentage)
    plt.title(title, fontsize=20)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel(title, fontsize=12)
    plt.ylim([0, 100])
    # caption
    plt.figtext(0.5, 0.02, description, wrap=True, horizontalalignment='center', fontsize=12)
    plt.tight_layout(pad=4)
    plt.show()


def startingCrawlerClass():
    os.remove("dump.txt")
    os.system("scrapy crawl mySpider2")


# starting crawler
startingCrawlerClass()

df = pd.read_csv("dump.txt", sep=',', names=["Indicator", "Ticker", "Year", "Amount"])
indicators = df.groupby("Indicator")

netEarning = []
revenue = []
grossProfit = []
year = []

for indicator, indicator_df in indicators:
    if indicator == 'net-income':
        netEarning = indicator_df['Amount'].values[0:10]
        year = indicator_df['Year'].values[0:10]
    if indicator == 'revenue':
        revenue = indicator_df['Amount'].values[0:10]
    if indicator == 'gross-profit':
        grossProfit = indicator_df['Amount'].values[0:10]

# Net Earning
netEarningPercent = calculatePercentage(obtained=netEarning, total=revenue)
showPercentChart(year=year, percentage=netEarningPercent, title='Net Earning in Percent',
                 description="Note: If a company is showing net earnings greater than 20% on total revenues, "
                             "it is probably benefiting from a long term competitive advantage.")
# Gross Profit
grossProfitMargin = calculatePercentage(obtained=grossProfit, total=revenue)
showPercentChart(year=year, percentage=grossProfitMargin, title='Gross Profit Margin',
                 description="Note: Firms with excellent long term economics tend to have consistently higher margin"
                             "margins. Greater than 40% = Durable competitive advantage. Less than 20% = no sustainable competitive advantage")
