import json
import pandas as pd
from matplotlib import pyplot as plt


def calculateNetEarning(netIncome, revenue):
    netEarningInPercent = []
    for i in range(0, len(netIncome)):
        netEarningInPercent.append(int((netIncome[i] / revenue[i]) * 100))
    return netEarningInPercent


def calculateGrowth(amount):
    revenue = [0]
    length = len(amount) - 1
    for i in range(0, length, 1):
        dividend = float(amount[i + 1]) - float(amount[i])
        divisor = float(amount[i])
        revenue.append(int((dividend / divisor) * 100))
    return revenue


def showNetEarningChart(year, netEarningInPercent):
    plt.plot(year, netEarningInPercent)
    plt.title("Net Earning in Percent", fontsize=20)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Net Earning in %', fontsize=12)
    plt.ylim([0, 100])
    # caption
    txt = "Note: If a company is showing net earnings greater than 20% on total " \
          "revenues, it is probably benefiting from a long term competitive advantage."
    plt.figtext(0.5, 0.02, txt, wrap=True, horizontalalignment='center', fontsize=12)
    plt.tight_layout(pad=4)
    plt.show()


def showRevenueChart(year, revenueGrowthInPercent):
    plt.plot(year, revenueGrowthInPercent)
    plt.title("Revenue Growth")
    plt.xlabel('Year')
    plt.ylabel('Revenue Growth %')
    # caption
    txt = "I need the caption to be present a little below X-axis"
    plt.figtext(0.5, 0.01, txt, wrap=True, horizontalalignment='center', fontsize=12)
    plt.tight_layout(pad=4)
    plt.show()


df = pd.read_csv("dump.txt", sep=',', names=["Indicator", "Ticker", "Year", "Amount"])
indicators = df.groupby("Indicator")

netEarning = []
revenue = []
year = []

for indicator, indicator_df in indicators:
    if indicator == 'net-income':
        netEarning = indicator_df['Amount'].values[0:10]
        year = indicator_df['Year'].values[0:10]
    if indicator == 'revenue':
        revenue = indicator_df['Amount'].values[0:10]

netEarningPercent = calculateNetEarning(netEarning, revenue)
showNetEarningChart(year, netEarningPercent)
