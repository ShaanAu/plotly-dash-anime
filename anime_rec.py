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
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import base64
import os
import statsmodels

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

email_input = html.Div(
    [
        dbc.FormGroup(
            [
                dbc.Label("Email"),
                dbc.Input(id="email-input", type="email", value=""),
                dbc.FormText("We only accept gmail..."),
                dbc.FormFeedback(
                    "That looks like a gmail address :-)", valid=True
                ),
                dbc.FormFeedback(
                    "Sorry, we only accept gmail for some reason...",
                    valid=False,
                ),
            ]
        )
    ]
)

form = dbc.Form(
    [
        dbc.FormGroup(
            [
                dbc.Label("Email", className="mr-2"),
                dbc.Input(type="email", placeholder="Enter email"),
            ],
            className="mr-3",
        ),
        dbc.FormGroup(
            [
                dbc.Label("Password", className="mr-2"),
                dbc.Input(type="password", placeholder="Enter password"),
            ],
            className="mr-3",
        ),
        dbc.Button("Submit", color="primary"),
    ],
    inline=True,
)


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


df_anime_new['episodes'] = df_anime_new.episodes.fillna(0)
df_anime_new.episodes.replace(('Unknown'), (0), inplace=True)
df_anime_new['episodes'] = df_anime_new.episodes.astype(int)
df_anime_new['episodes']=df_anime_new['episodes'].replace(0,df_anime_new['episodes'].mean())


for column in ['type','rating']:
    df_anime_new[column].fillna(df_anime_new[column].mode()[0], inplace=True)




figure_trendlines = px.scatter(df_anime_new, x="episodes", y="rating",trendline="ols")


figure_heatmap = go.Figure(data=go.Heatmap(
        z=df_anime_new_corr,
        x=df_anime_new_corr.columns,
        y=df_anime_new_corr.columns,
        colorscale='Viridis'))


sound_filename = path + '/plotly_dash_anime/anime.mp3'  # replace with your own .mp3 file
encoded_sound = base64.b64encode(open(sound_filename, 'rb').read())




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
    className="left_menu_3",
    children=[
        html.Div(

            html.Button(id="button1", children="Click me for sound")



        ),
        html.Div(id="placeholder", style={"display": "none"})
    ]
),


html.Div(
    className="right_content",
    children=[
        html.Div(
            className="header",
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
            ]
        ),

    ]
),



html.Div(
    className="top_metrics_50",
    children=[
        html.Div(

            dcc.Graph(figure=figure_trendlines)

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


html.Div(
    className="left_side_2",
    children=[
        html.Div(
            dcc.Graph(figure=figure_heatmap)
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

@app.callback(Output("placeholder", "children"),
              [Input("button1", "n_clicks")],
)
def play(n_clicks):
    if n_clicks is None:
        n_clicks = 0
    if n_clicks != 0:
        return html.Audio(src='data:audio/mpeg;base64,{}'.format(encoded_sound.decode()),
                          controls=False,
                          autoPlay=True,
                          )
        n_clicks = 0

# @app.callback(
#     [Output("email-input", "valid"), Output("email-input", "invalid")],
#     [Input("email-input", "value")],
# )
# def check_validity(text):
#     if text:
#         is_gmail = text.endswith("@gmail.com")
#         return is_gmail, not is_gmail
#     return False, False

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
