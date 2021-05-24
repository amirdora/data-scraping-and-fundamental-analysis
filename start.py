import dash

app = dash.Dash(__name__, suppress_callback_exceptions=True)
if __name__ == '__main__':
    app.run_server(debug=True)
