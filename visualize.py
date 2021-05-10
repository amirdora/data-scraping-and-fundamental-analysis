import os
import pandas as pd
from matplotlib import pyplot as plt
import linkGenerator


def setTickerAndGenerateLinks():
    ticker = 'GOOG'
    linkGenerator.generateLinks(ticker)


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
    # remove old file if exists
    fileName = "dump.txt"
    if os.path.exists(fileName):
        os.remove(fileName)
    os.system("scrapy crawl stockSpider")


# generating links
setTickerAndGenerateLinks()

# starting crawler
startingCrawlerClass()

df = pd.read_csv("dump.txt", sep=',', names=["Indicator", "Ticker", "Year", "Amount"])
indicators = df.groupby("Indicator")

netEarning = []
revenue = []
grossProfit = []
year = []
sga_expenses = []
research_expenses = []

for indicator, indicator_df in indicators:
    if indicator == 'net-income':
        netEarning = indicator_df['Amount'].values[0:10]
        year = indicator_df['Year'].values[0:10]
    if indicator == 'revenue':
        revenue = indicator_df['Amount'].values[0:10]
    if indicator == 'gross-profit':
        grossProfit = indicator_df['Amount'].values[0:10]
    if indicator == 'selling-general-administrative-expenses':
        sga_expenses = indicator_df['Amount'].values[0:10]
    if indicator == 'research-development-expenses':
        research_expenses = indicator_df['Amount'].values[0:10]

# net-income
netEarningPercent = calculatePercentage(obtained=netEarning, total=revenue)
showPercentChart(year=year, percentage=netEarningPercent, title='Net Earning in Percent',
                 description="Note: If a company is showing net earnings greater than 20% on total revenues, "
                             "it is probably benefiting from a long term competitive advantage.")
# gross-profit
grossProfitMargin = calculatePercentage(obtained=grossProfit, total=revenue)
showPercentChart(year=year, percentage=grossProfitMargin, title='Gross Profit Margin',
                 description="Note: Firms with excellent long term economics tend to have consistently higher margins."
                             " Greater than 40% = Durable competitive advantage. Less than 20% = no sustainable competitive advantage")

# selling-general-administrative-expenses
SGA_Percent_OfProfitMargin = calculatePercentage(obtained=sga_expenses, total=grossProfit)
showPercentChart(year=year, percentage=SGA_Percent_OfProfitMargin, title='SG&A Expenses in percent',
                 description="Note: Companies with no durable competitive advantage show wild variation in "
                             "SG&A as % of gross profit. Less than 30% is fantastic. Nearing 100% is in highly competitive industrye")

# research-development-expenses
research_expenses_OfProfitMargin = calculatePercentage(obtained=research_expenses, total=grossProfit)
showPercentChart(year=year, percentage=research_expenses_OfProfitMargin, title='R&D Expenses in percent',
                 description="High R&D usually threatens the competitive advantage. Buffett believes that companies that spend huge sums of money on R&D may develop an advantage, however, that advantage is bound to erode.")
