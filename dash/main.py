# # YouthMappers Activity Report
#
# # Import packages
# from dash import Dash, html, dash_table, dcc, callback, Output, Input
# import plotly.express as px
# import pandas as pd
#
#
# df = pd.read_csv('C:/Users/mowus/Documents/GWU/youthmappers/YM_github/dash/base_data/HOT_data_may23.csv')
#
#
# # Initialize the app
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# app = Dash(__name__)
#
# # App layout
# app.layout = html.Div([
#     html.Div(children='YouthMappers',
#              style={'textAlign': 'center', 'color': 'SlateGrey', 'fontSize': 30}),
#     html.Div(className='row', children=[
#             dcc.RadioItems(options=['percentMapped', 'percentValidated'],
#                            value='percentMapped',
#                            inline=True,
#                            id='my-radio-buttons-final')
#     ]),
#
#     html.Div(className='row', children=[
#         html.Div(className='six columns', children=[
#             dash_table.DataTable(data=df.to_dict('records'), page_size=11, style_table={'overflowX': 'auto'})
#         ]),
#         html.Div(className='six columns', children=[
#             dcc.Graph(figure={}, id='histo-chart-final')
#         ])
#     ])
#
# ])
# # Add controls to build the interaction
# @callback(
#     Output(component_id='histo-chart-final', component_property='figure'),
#     Input(component_id='my-radio-buttons-final', component_property='value')
# )
#
# def update_graph (col_chosen):
#     fig = px.histogram(df, x='status', y=col_chosen, histfunc='avg')
#     return fig
#
#
# # Run the app
# if __name__ == '__main__':
#     app.run_server(debug=True)