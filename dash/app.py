"""
YouthMappers Dashboard Web App.
This is an analytical dashboard for measure and monitor YouthMappers activities.

"""

# Import libraries
# # Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

import pandas as pd
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta


# Load data
HOT_df = pd.read_csv('C:/Users/mowus/Documents/GWU/youthmappers/YM_github/dash/base_data/HOT_data_may23.csv', parse_dates=['date'])

# ----------------------- Preprare data  -----------------------------------------------------------------------------------------------
# Assuming your data is stored in a Pandas DataFrame called df
HOT_df['date'] = pd.to_datetime(HOT_df['date'])  # Convert date column to datetime format
HOT_df['year'] = HOT_df['date'].dt.to_period('6M')  # Add new column with half-year periods

# ----------------------- Preprare data  -----------------------------------------------------------------------------------------------
def total_projects (data):
    total = data["projectsID"].count()
    return total

total_projects = total_projects(HOT_df)
# print(total_projects)

# Count the values in each half-year period
counts_year_status = HOT_df.groupby(['year', 'status']).count().reset_index()
# print(counts_year_status)
# Convert Period to string
counts_year_status['year'] = counts_year_status['year'].astype(str)

# Plot Line graph
fig_line = px.line(counts_year_status, x=counts_year_status.year, y=counts_year_status.projectsID, title='Project Creation Time Series')
fig_pie = px.pie(counts_year_status, values=counts_year_status.projectsID, names='status', title='Overall status')



# --------------------------------------------- Initial App --------------------------------------------------------------------------
# initial App
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# app = Dash(__name__, external_stylesheets=external_stylesheets)
app = Dash(__name__, external_stylesheets=[dbc.themes.MINTY],
           meta_tags=[{'name': 'viewport',
                       'content': 'width=device-width, initial-scale=1.0'}]
           )  # make app responsive

# --------------------------------------------- logo begin --------------------------------------------------------------------------
# add YM logo
logo = html.Img(className="align-items-center", alt="Thumbnail image", src="/assets/YM_logo1.jpg",
                style={"margin-left": "200px", 'padding-top': '100px'}, height="170px")
#
# # --------------------------------------------- Heading --------------------------------------------------------------------------
heading_title = html.Div([html.H2("Dashboard", className="display-4",
                                  style={"display": "inline-block", "text-align": "center", "margin-left": "200px",
                                         'padding-top': '100px'})])

# --------------------------------------------- sidebar begin --------------------------------------------------------------------------
# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    'padding-top': '50px',
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    'padding-top': '100px',
}

sidebar = html.Div(
    [
        html.H2("Pages", className="display-7"),
        html.Hr(),
        html.P(
            "Select HOT or TEACH tasking manager", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("HOME", href="/", active="exact"),
                dbc.NavLink("HOT TM", href="/HOT-TM", active="exact"),
                dbc.NavLink("TEACH TM", href="/TEACH-TM", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

# --------------------------------------------- sidebar end --------------------------------------------------------------------------


app.layout = dbc.Container([

    dbc.Row([
        dbc.Col([
            html.Div([logo, heading_title], className="header",
                     style={"text-align": "center", "display": "flex", "align-items": "center", "height": "55px"}),
        ])
    ]),


    html.Div([dcc.Location(id="url"), sidebar, content]),

    dbc.Row([
        # total projects
        dbc.Col([html.P(" Total projects"), html.H1(f"{total_projects}")], width=2),
        # sliders here
    ], style={"margin-left": "200px", 'display': 'flex', 'flex-direction': 'row'}),

    dbc.Row([

        # pie chart
        dbc.Col([ dcc.Graph(id='pie-chart', figure=fig_pie)],width=5, className="col",
                     style={"width": "39%", "border-right": "1px solid #ccc"}),
        dbc.Col([dcc.Graph(id='line-chart', figure=fig_line)],  className="col",
                style={"width": "50%", "border-right": "1px solid #ccc"}),
        ], style={"margin-left": "200px", 'display': 'flex', 'flex-direction': 'row'})

    # dbc.Row([
    #     dbc.Col([
    #         html.Div([dcc.Graph(figure={})], className="col",
    #                  style={"width": "20%", "border-right": "1px solid #ccc"}),
    #         html.Div([dcc.Graph(figure={})], className="col",
    #                  style={"width": "30%", "border-right": "1px solid #ccc"}),
    #         html.Div([dcc.Graph(figure={})], className="col",
    #                  style={"width": "50%", "border-right": "1px solid #ccc"}),
    #     ], style={"margin-left": "200px", 'display': 'flex', 'flex-direction': 'row'})
    # ])
])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return html.H3("HOME")
    elif pathname == "/HOT-TM":
        return html.H3("HOT Tasking Manager")
    elif pathname == "/TEACH-TM":
        return html.H3("TEACH Tasking Manager")
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )

# Define the callback function to update the pie chart
# @app.callback(
#     Output('pie-chart', 'figure'),
#     [Input('line-chart', 'clickData')]
# )
# def update_pie_chart(click_data):
#     if click_data is not None:
#         # Get the date clicked by the user
#         date = click_data['points'][0]['x']
#
#         # Filter the data to show only the selected date
#         filtered_df = counts_year_status[counts_year_status['status'] == date]
#
#         # Create the pie chart
#         fig = px.pie(filtered_df, values='projectsID', names='projectsID')
#         fig.update_layout(title=f'Pie Chart for {date}')
#         return fig
#     else:
#         # If no date is selected, show the overall pie chart
#         fig = fig_pie
#         fig.update_layout(title='Overall ')
#         return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
