import dash
import dash_table
import pandas as pd
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
import requests


development = go.Figure(data=[go.Scatter(x=[1, 2, 3, 4], y=[0, 1, 20, 200])])

r = requests.get('https://thevirustracker.com/free-api?countryTotal=BR').json()
country_data = r.get('countrydata',[])
country_data = country_data[0]
del country_data['info']
country_data = pd.DataFrame([country_data.values()],columns=country_data.keys())
country_news = r.get('countrynewsitems',[])[0]
country_news = pd.DataFrame(country_news).transpose()

news_feed = []
md = []
for title,link in country_news[['title','url']].values:
    md.append("[{}]({})".format(title,link))
news_feed = '\n\n'.join(md)


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
external_stylesheets = ["assets/dark.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    [
        html.Div(
            className="app-header",
            children=[
                html.H1("Estatísticas coronavírus no Brasil"),
                dash_table.DataTable(
                    id="country_data",
                    columns=[{"name": i, "id": i} for i in country_data.columns],
                    data=country_data.to_dict("records"),
                ),
                dcc.Graph(id="development", figure=development),
                html.H2("notícias"),
                dcc.Markdown(news_feed),
            ],
        )
    ]
)

if __name__ == "__main__":

    app.run_server(host='0.0.0.0',debug=True)
