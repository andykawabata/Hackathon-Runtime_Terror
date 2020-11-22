# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
from datetime import date
import pandas as pd
import plotly.express as px
from classes.read_csv import Data
from classes.predictive_plot import PredictivePlot
from classes.actual_plot import ActualPlot
from classes.label_mapper import LabelMapper

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

filenames_labels = LabelMapper.map_to_array()
locations = []
files = Data().get_all_file_names()

# BUILD LABELS AND VALUES FOR BUILDING SELECTION DROPDOWN
for pair in filenames_labels:
    locations.append({'label': pair['label'], 'value': pair['filename']})

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
        value=filenames_labels[0]['filename'],
        multi=True
    ),
    dcc.RadioItems(
                id='time-select-pred',
                options=[
                    {'label': 'Hourly', 'value': 'Hour'},
                    {'label': 'Daily', 'value': 'Day'},
                    {'label': 'Weekly', 'value': 'Week'},
                    {'label': 'Monthly', 'value': 'Month'}
                ],
                value='Day',
                labelStyle={'display': 'inline-block'}
            ),
    html.Div(id='output-container-date-picker-range'),
    html.Div(id='predictive-graph-container', children=[]),
    dcc.Dropdown(
        id='building-names-pred',
        options=locations,
        value=filenames_labels[0]['filename'],
        multi=False
    ),
])


@app.callback(
    dash.dependencies.Output('actual-graph-container', 'children'),
    [dash.dependencies.Input('building-names', 'value'),
     dash.dependencies.Input('time-select', 'value')])
def update_output(filenames, time_select):
    """
    This callback fires when the building-names dropdown, and time period
    selection fields are changed in the view
    :param filenames: names of files to be rendered into graphs
    :param labels: labels associated with filename
    :param time_select: hourly, daily, weekly, monthly
    :return: a single of multi-line graph based on the inputs
    """
    graph = ActualPlot.build_graph(filenames, time_select)
    return graph

@app.callback(
    dash.dependencies.Output('predictive-graph-container', 'children'),
    [dash.dependencies.Input('building-names-pred', 'value'),
     dash.dependencies.Input('time-select-pred', 'value')])
def update_output(filename, time_select_pred):
    predictive_graph = PredictivePlot(filename[0])
    graph = predictive_graph.create_graph2(Data().get_df_for_file(filename), time_select_pred)
    return graph

if __name__ == '__main__':
    app.run_server(debug=True)
