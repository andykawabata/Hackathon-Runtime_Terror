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
predictive_graph = PredictivePlot(files[0])
graph = predictive_graph.create_graph2()

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
    dcc.DatePickerRange(
        id='my-date-picker-range',
        min_date_allowed=date(2020, 1, 1),
        max_date_allowed=date(2020, 9, 19),
        initial_visible_month=date(2020, 1, 5),
        start_date=date(2020, 1, 1),
        end_date=date(2020, 1, 31)
    ),
    dcc.RadioItems(
                id='time-select-pred',
                options=[
                    {'label': 'Hourly', 'value': 'Hour'},
                    {'label': 'Daily', 'value': 'Day'},
                    {'label': 'Weekly', 'value': 'Week'},
                    {'label': 'Monthly', 'value': 'Month'}
                ],
                value='daily',
                labelStyle={'display': 'inline-block'}
            ),
    html.Div(id='output-container-date-picker-range'),
    html.Div(id='predictive-graph-container', children=[]),
    # graph
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
    [dash.dependencies.Input('building-names', 'value'),
     dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date'),
     dash.dependencies.Input('time-select-pred', 'value')])
def update_output(filenames, start_date, end_date, time_select_pred):
    string_prefix = 'You have selected: '
    
    predictive_graph = PredictivePlot(filenames[-1])

    if start_date is not None:
        start_date_object = date.fromisoformat(start_date)
        start_date_string = start_date_object.strftime('%B %d, %Y')
    if end_date is not None:
        end_date_object = date.fromisoformat(end_date)
        end_date_string = end_date_object.strftime('%B %d, %Y')
    if start_date is not None and end_date is not None and time_select_pred is not None:
        graph = predictive_graph.create_graph2(start_date_string, end_date_string, time_select_pred)
        return graph
    # if time_select_pred is not None:
    #     graph = predictive_graph.create_graph2(time_select_pred)
    #     return graph
    else:
        graph = predictive_graph.create_graph2()
        return graph

if __name__ == '__main__':
    app.run_server(debug=True)
