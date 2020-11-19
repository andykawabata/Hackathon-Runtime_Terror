# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from classes.read_csv import Data
from classes.predictive_plot import PredictivePlot
from classes.actual_plot import ActualPlot

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

reader = Data()
names = reader.get_all_file_names()
labels = [filename.split('_')[0] for filename in names]
locations = []

predictive_graph = PredictivePlot(names[0])

#BUILD LABELS AND VALUES FOR BUILDING SELECTION DROPDOWN
for i in range(0, len(names)):
    locations.append({'label': labels[i], 'value': names[i]})

app.layout = html.Div(style={'margin': '0  300px' }, children=[
    dcc.RadioItems(
                id='time-select',
                options=[
                    {'label': 'Hourly', 'value': 'hourly'},
                    {'label': 'Daily', 'value': 'daily'},
                    {'label': 'Weekly', 'value': 'weekly'},
                    {'label': 'Monthly', 'value': 'monthly'}
                ],
                value='daily',
                labelStyle={'display': 'inline-block'}
            ),
    html.Div(id='actual-graph-container', children=[]),
    dcc.Dropdown(
        id='building-names',
        options=locations,
        value=names[0],
        multi=True
    ),
    predictive_graph.create_graph()
])


@app.callback(
    dash.dependencies.Output('actual-graph-container', 'children'),
    [dash.dependencies.Input('building-names', 'value'),
     dash.dependencies.Input('time-select', 'value')])
def update_output(filenames, time_select):
    graph = ActualPlot.build_graph(filenames, time_select)
    return graph


if __name__ == '__main__':
    app.run_server(debug=True)
