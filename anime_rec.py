#Import packages and libraries
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import base64
import os

# path = '/Users/shaanaucharagram/Documents/repos/plotly_dash_anime'
#
# image_filename = path + '/data/marker.png' # replace with your own image
# encoded_image = base64.b64encode(open(image_filename, 'rb').read())

app = dash.Dash(__name__)

#############################################div for main bar#####################################################

app.layout = html.Div([
    html.Div([
        html.Img(
            src = app.get_asset_url('marker.png'),
            style={'height': '100px'},

        )

    ],
        className='four columns',
        style={"display":"inline-block"}),

    html.Div([
        html.H1("Anime Dashboard",
            style={ 'height': '50%',
                    "fontSize":85,
                    "color":"white",})


    ],
        className='six columns',
        style={"display":"inline-block"})

],
    className="row header",
    style={"backgroundColor": "red", "height" : "200px", 'justify-content': 'center', 'justify-content': 'center', 'align-items': 'center','display': 'flex'})


if __name__ == '__main__':
    app.run_server(debug=True)