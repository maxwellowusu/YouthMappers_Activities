#
# # Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input, State
import plotly.express as px
import plotly.graph_objects as go

import pandas as pd
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta

# Load data
df = pd.read_csv('C:/Users/mowus/Documents/GWU/youthmappers/YM_github/dash/base_data/HOT_data_may23.csv', parse_dates=['date'])

# Mapbox
coor = pd.read_csv('C:/Users/mowus/Documents/GWU/youthmappers/YM_github/dash/base_data/HOT_coordinates_may23.csv')
fig = go.Figure(go.Densitymapbox(lat=coor.lat, lon=coor.lon, z=coor.projectsID,
                                 radius=10))
fig.update_layout(mapbox_style="open-street-map", mapbox_center_lon=0)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# fig.show()

###########################################################
# Define the date range
date_range = [df['date'].min(), df['date'].max()]

# Define the slider with timestamps
slider = dcc.RangeSlider(
    id='time-slider',
    min=date_range[0].timestamp(),
    max=date_range[1].timestamp(),
    step=relativedelta(months=3).seconds,
    value=[date_range[0].timestamp(), date_range[1].timestamp()],
    marks={int(dt.timestamp(dt(year=y, month=m, day=1))): f"{m}/{y}" for y in range(date_range[0].year, date_range[1].year+1) for m in range(1, 13, 3)}
)
#############################################################

total_project = df['projectsID'].value_counts()

#############################################################

fig_pie = px.pie(df, values=total_project, names='status', title='Overall status')
fig_line = px.line(df, x="date", y=total_project, title='line')

#############################################################

# add YM logo
logo = html.Img(src="/assets/YM_logo.png", height="150px")

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div\
        ([
        html.Div([logo, html.H2("Dashboard", style={"display": "inline-block", "margin-left": "50px"})], className="header",
                 style={"text-align": "center", "display": "flex", "align-items": "center", "height": "55px"}),

        html.Br(),
            html.Div([slider]),

        html.Br(),
        html.Div([
            html.Br(),
            html.Div([dcc.Graph(figure=fig_pie)], className="col", style={"width": "20%", "border-right": "1px solid #ccc"}),
            html.Div([dcc.Graph(figure=fig_line)], className="col", style={"width": "50%", "border-right": "1px solid #ccc"}),
            html.Div([dcc.Graph(figure=fig)], className="col", style={"width": "50%", "border-right": "1px solid #ccc"}),
        ],  style={'display': 'flex', 'flex-direction': 'row'}),

        html.Div([
            html.Br(),
            html.Div([dcc.Graph({})], className="col", style={"width": "20%", "border-right": "1px solid #ccc"}),
            html.Div([dcc.Graph({})], className="col", style={"width": "50%", "border-right": "1px solid #ccc"}),
            html.Div([dcc.Graph({})], className="col", style={"width": "50%", "border-right": "1px solid #ccc"}),
        ], style={'display': 'flex', 'flex-direction': 'row'}),

        dcc.Input(id='input-1', type='number', value=total_project),
        html.H2(id='output')

        ])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

