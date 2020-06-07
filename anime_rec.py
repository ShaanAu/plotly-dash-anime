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

os.chdir('/Users/shaanaucharagram/Documents/repos/plotly_dash_anime')

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



path = '/Users/shaanaucharagram/Documents/repos'
anime_df = pd.read_csv(path + "/big_data/anime.csv")
rating_df = pd.read_csv(path + "/big_data/rating.csv")
df = pd.get_dummies(anime_df, columns=['type'])
df_anime_new = pd.merge(anime_df, df)
df_anime_new_corr = df_anime_new.corr()

rating_df['did_rate'] = np.where(rating_df['rating']!=-1, 1, 0)
test_df = anime_df.merge(rating_df, on='anime_id', how='left')
test_df['count'] = test_df['anime_id'].map(test_df['anime_id'].value_counts())

genres = pd.DataFrame(anime_df.genre.str.split(',', expand=True).stack(), columns=['genre'])
genres = genres.reset_index(drop=True)
genre_count = pd.DataFrame(genres.groupby(by=['genre']).size(), columns=['count'])
genre_count = genre_count.reset_index()

top_20 = genre_count.nlargest(20, 'count')
top_10 = genre_count.nlargest(10, 'count')
top_5 = genre_count.nlargest(5, 'count')


figure_bar = px.bar(top_20, x='genre', y='count')

fig_box = px.box(anime_df, x="type", y="rating")


figure_heatmap = go.Figure(data=go.Heatmap(
        z=df_anime_new_corr,
        x=df_anime_new_corr.columns,
        y=df_anime_new_corr.columns,
        colorscale='Viridis'))



# image_filename = path + '/data/marker.png' # replace with your own image
# encoded_image = base64.b64encode(open(image_filename, 'rb').read())

app = dash.Dash(__name__,
                external_scripts=external_scripts,
                external_stylesheets=external_stylesheets
                )

#############################################div for main bar#####################################################
app.layout = html.Div(
            className="content",
            children=[

html.Div(
    className="left_menu",
    children=[
        html.Div(
            daq.Gauge(
                color={"gradient":True,"ranges":{"yellow":[0,5],"orange":[5,7],"red":[7,10]}},
                label="Default",
                value=5
             ),
        ),
    ]
),


html.Div(
    className="left_menu_2",
    children=[
        html.Div(
            daq.Gauge(
                    id='my-gauge',
                    label="Default",
                    value=6
            ),
        ),
        dcc.Slider(
            id='my-gauge-slider',
            min=0,
            max=10,
            step=1,
            value=5
        ),
    ]
),

html.Div(
    className="right_content",
    children=[
        html.Div(
            className="top_metrics",
            children=[
                html.Div([
                    html.H1("Anime Dashboard",
                    style={ "font-family": "Helvetica",
                            "fontSize":90,
                            "color":"orange",
                            'background-image': 'url(/assets/test1.jpeg)',
                            'justify-content': 'center',
                            'align-items': 'center',
                            'display': 'flex'})
                ]),
                html.Div(
                    'This down top metrics'
                ),
            ]
        ),

    ]
),

html.Div(
    className="top_metrics_50",
    children=[
        html.Div(
            dcc.Slider(
                min=0,
                max=10,
                step=None,
                marks={
                    1: '10 °F',
                    3: '3 °F',
                    5: '5 °F',
                    6: '7.65 °F',
                    10: '10 °F'
                },
                value=5
            ),
        ),
    ]
),

html.Div(
    className="left_side",
    children=[
        html.Div(
            dcc.Graph(id='bar')
        ),
    ]
),


    ])

@app.callback(
    Output('bar', 'figure'),
    [Input('my-gauge-slider','value')])
def update_graph(slider):
    top_n_bar = genre_count.nlargest(slider, 'count')
    figure_bar = px.bar(top_n_bar, x='genre', y='count')


    return figure_bar
# #
@app.callback(
    dash.dependencies.Output('my-gauge', 'value'),
    [dash.dependencies.Input('my-gauge-slider', 'value')]
)
def update_output(value):
    return value

if __name__ == '__main__':
    app.run_server(debug=True)






# app.layout = html.Div([
# ###############################Div for header####################################################################
# html.Div([
#     html.Div([
#         html.H1("Anime Dashboard",
#             style={ "font-family": "Helvetica",
#                     "fontSize":90,
#                     "color":"orange",})
#
#
#     ],
#         className='six columns',
#         style={"display":"inline-block"})
#
# ],
#     className="row header",
#     style={'background-image': 'url(/assets/test1.jpeg)','justify-content': 'center', 'align-items': 'center','display': 'flex'}),
#
#
#      html.Div([
#         html.Div([
#             daq.Gauge(
#                 id='my-gauge',
#                 color={"gradient":True,"ranges":{"yellow":[0,5],"orange":[5,7],"red":[7,10]}},
#                 label="Default",
#                 value=5
#              ),
#             dcc.Slider(
#                 id = 'slider',
#                 min=5,
#                 max=15,
#                 step=None,
#                 verticalHeight=200,
#                 vertical=True,
#                 marks={
#                     5: 'Top 5',
#                     10: 'Top 10',
#                     15: 'Top 20',
#                 },
#                 value=5,
#             )
#         ], className= "left_menu"),
#
#         html.Div([
#             dcc.Graph(id='bar')
#         ], className= "left_menu"),
#
#         html.Div([
#             dcc.Graph(figure=fig_box)
#         ], className= "five columns")
#
#         ],className='row'),
#
#
#     html.Div([
#         html.Div([
#             dcc.Graph(figure=figure_heatmap)
#
#         ], className='four columns')
#
#
#     ], className='row')
#
#     ])
#
#
@app.callback(
    Output('bar', 'figure'),
    [Input('my-gauge-slider','value')])
def update_graph(slider):
    top_n_bar = genre_count.nlargest(slider, 'count')
    figure_bar = px.bar(top_n_bar, x='genre', y='count')


    return figure_bar
# #
@app.callback(
    dash.dependencies.Output('my-gauge', 'value'),
    [dash.dependencies.Input('my-gauge-slider', 'value')]
)
def update_output(value):
    return value


# @app.callback(
#     Output('pie', 'figure'),
#     [Input('slider','value')])
# def update_graph(slider):
#     if slider == 5:
#         figure_bar = px.bar(top_5, x='genre', y='count')
#     elif slider == 10:
#         figure_bar = px.bar(top_10, x='genre', y='count')
#     elif slider == 15:
#         figure_bar = px.bar(top_20, x='genre', y='count')
#
#     return figure_bar





# if __name__ == '__main__':
#     app.run_server(debug=True)
