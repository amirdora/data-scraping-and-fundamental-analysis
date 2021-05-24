import os
import sys

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import linkGenerator
from app import app
from apps import dash

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Br(),
    html.H1("Interpretation of Financial Statements", style={'text-align': 'center'}),
    html.H1("10 year data analysis", style={'text-align': 'center'}),
    html.Div(id='input-container',
             children=[dcc.Input(id='input-1-state', type='text', placeholder="Enter Company Ticker", value=''),
                       dcc.Input(id='input-2-state', type='text', placeholder="Enter Company Name", value=''),
                       dcc.Link(' Get Analytics ', href='/apps/dash')]),
    html.Div(id='display-page'),
    html.Div([html.Footer('Copyright © 2021 Amir Dora. - All Rights Reserved.')],
             style={"position": "absolute", "bottom": "0"}),

], style={"margin-left": "5%", "margin-right": "5%"})


@app.callback(Output(component_id='display-page', component_property='children'),
              Output(component_id='input-container', component_property='style'),
              [Input(component_id='url', component_property='pathname')],
              Input(component_id='input-1-state', component_property='value'),
              Input(component_id='input-2-state', component_property='value'))
def display_page(pathname, ticker, company):
    if pathname == '/apps/dash':

        # generate links
        linkGenerator.generateLinks(ticker, company)

        # starting crawler
        startingCrawlerClass()

        return dash.layout, {'display': 'none'}
    else:
        return '', {'display': 'block'}


def startingCrawlerClass():
    # remove old file if exists
    fileName = "dump.txt"
    if os.path.exists(fileName):
        os.remove(fileName)
    os.system("scrapy crawl stockSpider")


if __name__ == '__main__':
    app.run_server(debug=True)
