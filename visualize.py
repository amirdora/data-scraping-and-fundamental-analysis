import json
import pandas as pd
from matplotlib import pyplot as plt

netEarningInPercent = []
revenue = [0]


def calculateNetEarning():
    for i in range(0, len(netIncome)):
        netEarningInPercent.append(int((netIncome[i] / revenue[i]) * 100))
    return netEarningInPercent


def calculateGrowth(amount):
    length = len(amount) - 1
    for i in range(0, length, 1):
        dividend = float(amount[i + 1]) - float(amount[i])
        divisor = float(amount[i])
        revenue.append(int((dividend / divisor) * 100))
    return revenue


def showNetEarningChart(year, netEarningInPercent):
    plt.plot(year, netEarningInPercent)
    plt.title("Net Earning in %")
    plt.xlabel('Year')
    plt.ylabel('Net Earning in %')
    # caption
    txt = "I need the caption to be present a little below X-axis"
    plt.figtext(0.5, 0.01, txt, wrap=True, horizontalalignment='center', fontsize=12)
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


with open('data.json', 'r') as f:
    data = json.load(f)
df = pd.DataFrame(data)

year = [i['year'] for i in df["Income"][0:9]]
revenue = [i['revenue'] for i in df['Income'][0:9]]
netIncome = [i['net-income'] for i in df['Income']]

year.reverse()
revenue.reverse()
netIncome.reverse()

netEarningInPercent = calculateNetEarning()

revenueGrowthInPercent = calculateGrowth(revenue)

showRevenueChart(year, revenueGrowthInPercent)
showNetEarningChart(year, netEarningInPercent)
