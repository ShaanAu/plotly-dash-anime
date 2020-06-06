#Import packages and librarie
import pandas as pd
import numpy as np
import dash_daq as daq
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
import plotly.graph_objects as go
import plotly.express as px
from dash.dependencies import Input, Output
import base64
import os

# external JavaScript files
external_scripts = [
    'https://www.google-analytics.com/analytics.js',
    {'src': 'https://cdn.polyfill.io/v2/polyfill.min.js'},
    {
        'src': 'https://cdnjs.cloudflare.com/ajax/libs/lodash.js/4.17.10/lodash.core.js',
        'integrity': 'sha256-Qqd/EfdABZUcAxjOkMi8eGEivtdTkh3b65xCZL4qAQA=',
        'crossorigin': 'anonymous'
    }
]

# external CSS stylesheets
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]



path = '/Users/shaanaucharagram/Documents/repos/plotly_dash_anime'
anime_df = pd.read_csv(path + "/data/anime.csv")
rating_df = pd.read_csv(path + "/data/rating.csv")
path = '/Users/shaanaucharagram/Documents/repos/plotly_dash_anime'

genres = pd.DataFrame(anime_df.genre.str.split(',', expand=True).stack(), columns=['genre'])
genres = genres.reset_index(drop=True)
genre_count = pd.DataFrame(genres.groupby(by=['genre']).size(), columns=['count'])
genre_count = genre_count.reset_index()

top_20 = genre_count.nlargest(20, 'count')
top_10 = genre_count.nlargest(10, 'count')
top_5 = genre_count.nlargest(5, 'count')


figure_bar = px.bar(top_20, x='genre', y='count')

fig_box = px.box(anime_df, x="type", y="rating")


# image_filename = path + '/data/marker.png' # replace with your own image
# encoded_image = base64.b64encode(open(image_filename, 'rb').read())

app = dash.Dash(__name__,
                external_scripts=external_scripts,
                external_stylesheets=external_stylesheets
                )

#############################################div for main bar#####################################################

app.layout = html.Div([
###############################Div for header####################################################################
html.Div([
    html.Div([
        html.H1("Anime Dashboard",
            style={ "font-family": "Helvetica",
                    "fontSize":90,
                    "color":"orange",})


    ],
        className='six columns',
        style={"display":"inline-block"})

],
    className="row header",
    style={'background-image': 'url(/assets/test1.jpeg)','justify-content': 'center', 'align-items': 'center','display': 'flex'}),


     html.Div([
        html.Div([
            dcc.Slider(
                id = 'slider',
                min=5,
                max=15,
                step=None,
                verticalHeight=200,
                vertical=True,
                marks={
                    5: 'Top 5',
                    10: 'Top 10',
                    15: 'Top 20',
                },
                value=5,
            )
        ], className= "one column", style={'margin-top':"100px", 'margin-left':'75px'}),

        html.Div([
            dcc.Graph(id='bar')
        ], className= "five columns"),

        html.Div([
            dcc.Graph(figure=fig_box)
        ], className= "five columns")

        ],className='row'),

     html.Div([
        
        html.Div([
            dcc.Graph(id = 'linreg')
        ], className= 'six columns')
        ])

    ])


@app.callback(
    Output('bar', 'figure'),
    [Input('slider','value')])
def update_graph(slider):
    if slider == 5:
        figure_bar = px.bar(top_5, x='genre', y='count')
    elif slider == 10:
        figure_bar = px.bar(top_10, x='genre', y='count')
    elif slider == 15:
        figure_bar = px.bar(top_20, x='genre', y='count')

    return figure_bar

@app.callback(
    Output('pie', 'figure'),
    [Input('slider','value')])
def update_graph(slider):
    if slider == 5:
        figure_bar = px.bar(top_5, x='genre', y='count')
    elif slider == 10:
        figure_bar = px.bar(top_10, x='genre', y='count')
    elif slider == 15:
        figure_bar = px.bar(top_20, x='genre', y='count')

    return figure_bar





if __name__ == '__main__':
    app.run_server(debug=True)