import os

import pandas as pd
import plotly.express as px  # (version 4.7.0)
import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from matplotlib import pyplot as plt
import linkGenerator

ticker = 'TSLA'
company = 'Tesla'


def setTickerAndGenerateLinks():
    linkGenerator.generateLinks(ticker, company)


def calculatePercentage(obtained, total):
    amountInPercent = []
    for i in range(0, len(obtained)):
        amountInPercent.append(int((obtained[i] / total[i]) * 100))
    return amountInPercent


def startingCrawlerClass():
    # remove old file if exists
    fileName = "dump.txt"
    if os.path.exists(fileName):
        os.remove(fileName)
    os.system("scrapy crawl stockSpider")


# ---------- start dash

app = dash.Dash(__name__)

# generating links
setTickerAndGenerateLinks()

# starting crawler
startingCrawlerClass()

# ---------- Import and clean data (importing csv into pandas)
df = pd.read_csv("dump.txt", sep=',', names=["Indicator", "Ticker", "Year", "Amount"])
indicators = df.groupby("Indicator")

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Interpretation of Financial Statements", style={'text-align': 'center'}),
    html.H1("10 year data analysis", style={'text-align': 'center'}),

    dcc.Dropdown(id="selection_type",
                 options=[
                     {"label": "Net Earning in Percent", "value": "net-income"},
                     {"label": "Gross Profit Margin", "value": "gross-profit"},
                     {"label": "SG&A Expenses in percent", "value": "selling-general-administrative-expenses"},
                     {"label": "R&D Expenses in percent", "value": "research-development-expenses"},
                     {"label": "Depreciation cost", "value": "total-depreciation-amortization-cash-flow"}],
                 multi=False,
                 value="net-income",
                 style={'width': "50%"}
                 ),

    html.Br(),
    html.Div(id='company_ticker', children=[]),
    html.Div(id='company_name', children=[]),
    dcc.Graph(id='percent_graph', figure={}),
    html.P(id='note_text', children=[], style={'text-align': 'center', 'color': 'orange'}),

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='note_text', component_property='children'),
     Output(component_id='percent_graph', component_property='figure')],
    [Input(component_id='selection_type', component_property='value'),
     Input(component_id='company_ticker', component_property='children'),
     Input(component_id='company_name', component_property='children')]
)
def update_graph(option_slctd, companyTicker, companyName):
    global noteText
    print(option_slctd)
    print(type(option_slctd))

    grossProfit, netEarning, research_expenses, revenue, sga_expenses, total_depreciation, year = parseDataFrame()

    # net-income
    if option_slctd == "net-income":
        netEarningPercent = calculatePercentage(obtained=netEarning, total=revenue)
        fig = generatePercentGraph("Net Earning in Percent", netEarningPercent, year)
        noteText = "Warren Buffett's Advice: If a company is showing net earnings greater than 20% on total revenues, " \
                   "it is probably benefiting from a long term competitive advantage."

    # gross-profit
    if option_slctd == "gross-profit":
        grossProfitMargin = calculatePercentage(obtained=grossProfit, total=revenue)
        fig = generatePercentGraph("Gross Profit Margin", grossProfitMargin, year)
        noteText = "Warren Buffett's Advice: Firms with excellent long term economics tend to have consistently higher margins. " \
                   "Greater than 40% = Durable competitive advantage. Less than 20% = no sustainable competitive " \
                   "advantage "

    # selling-general-administrative-expenses
    if option_slctd == "selling-general-administrative-expenses":
        SGA_Percent_OfProfitMargin = calculatePercentage(obtained=sga_expenses, total=grossProfit)
        fig = generatePercentGraph("SG&A Expenses in percent", SGA_Percent_OfProfitMargin, year)
        noteText = "Warren Buffett's Advice: Companies with no durable competitive advantage show wild variation in " \
                   "SG&A as % of gross profit. Less than 30% is fantastic. Nearing 100% is in highly competitive " \
                   "industry "

    # research-development-expenses
    if option_slctd == "research-development-expenses":
        research_expenses_OfProfitMargin = calculatePercentage(obtained=research_expenses, total=grossProfit)
        fig = generatePercentGraph("R&D Expenses in percent", research_expenses_OfProfitMargin, year)
        noteText = "Warren Buffett's Advice: High R&D usually threatens the competitive advantage. Buffett believes that companies that " \
                   "spend huge sums of money on R&D may develop an advantage, however, that advantage is bound to " \
                   "erode. "

    # total-depreciation-amortization-cash-flow
    if option_slctd == "total-depreciation-amortization-cash-flow":
        depreciation_cost_inPercent = calculatePercentage(obtained=total_depreciation, total=grossProfit)
        fig = generatePercentGraph("Depreciation cost", depreciation_cost_inPercent, year)
        noteText = "Warren Buffett's Advice: Companies with durable competitive advantages tend to have lower depreciation costs as a % " \
                   "of gross profit. Coca Cola has consistent 6% depreciation which is considered good. "

    return noteText, fig


def parseDataFrame():
    netEarning = []
    revenue = []
    grossProfit = []
    year = []
    sga_expenses = []
    research_expenses = []
    total_depreciation = []
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
        if indicator == 'total-depreciation-amortization-cash-flow':
            total_depreciation = indicator_df['Amount'].values[0:10]
    return grossProfit, netEarning, research_expenses, revenue, sga_expenses, total_depreciation, year


def generatePercentGraph(title, percentRange, year):
    yLowestRange = lambda minValue: minValue if minValue < 0 else 0

    global fig
    fig = px.line(x=year, y=percentRange)
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title=title,
        yaxis_range=[yLowestRange(min(percentRange)), 100],
        title_text=company + " - " + title,
        title_xanchor="center",
        title_font=dict(size=24),
        title_x=0.5,
    )
    return fig


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
