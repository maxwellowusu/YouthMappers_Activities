import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html

# import dash
# import dash_core_components as dcc
# import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        # Sidebar
        html.Div([
            html.H2('Sidebar'),
            # Add other sidebar content here
        ], className='sidebar'),

        # Main content area
        html.Div([
            html.H1('Main Content'),
            dcc.Graph(id='my-graph'),
        ], className='content'),

    ], className='wrapper'),
])


# @app.callback(Output('my-graph', 'figure'), [Input('...', '...')])
# def update_graph(...):
#     # Add code to update graph here
#     pass


if __name__ == '__main__':
    app.run_server(debug=True)
