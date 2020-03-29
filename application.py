import dash
import dash_table
import pandas as pd
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
import requests
import time
import csv

data = pd.read_csv('Historic Data_17_03_20.csv', delimiter=";",encoding='latin-1')
data_brazil = data.loc[(data['countrycode']=="BR")]

data_brazil = data_brazil[data_brazil["totalcases"]>0.]

data_brazil['date'] = pd.to_datetime(data_brazil['date'])
development = go.Figure(data=[go.Scatter(x=data_brazil["date"], y=data_brazil["totalcases"])])

def fetch_data():
    r = requests.get("https://thevirustracker.com/free-api?countryTotal=BR", headers={"User-Agent": "XY"})
    r = r.json()

    country_data = r.get('countrydata',[])
    country_data = country_data[0]
    del country_data['info']
    country_data = pd.DataFrame([country_data.values()],columns=country_data.keys())
    return country_data
#country_news = r.get('countrynewsitems',["No news"])[0]
#country_news = pd.DataFrame(country_news).transpose()

#news_feed = []
#md = []
#for title,link in country_news[['title','url']].values:
#    md.append("[{}]({})".format(title,link))
#news_feed = '\n\n'.join(md)


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
external_stylesheets = ["assets/dark.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#news_feed = []
application = app.server

update_seconds = 30
app.layout = html.Div(
    [
        html.Div(
            className="app-header",
            children=[
                html.H1("Estatísticas coronavírus no Brasil"),
                dcc.Interval('graph-update',interval = update_seconds * 1000, n_intervals = 0),
                dash_table.DataTable(
                    id="country_data",
                    columns=[{"name": i, "id": i} for i in fetch_data().columns],
                    data=fetch_data().to_dict("records"),
                ),
                dcc.Graph(id="development", figure=development),
                html.H2("notícias"),
                #dcc.Markdown(news_feed),
            ],
        )
    ]
)

if __name__ == "__main__":
    application.run(debug=False, port=8080)



