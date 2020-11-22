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
# predictive_graph = PredictivePlot(files[0])
# graph = predictive_graph.create_graph('Week')

# BUILD LABELS AND VALUES FOR BUILDING SELECTION DROPDOWN
for pair in filenames_labels:
    locations.append({'label': pair['label'], 'value': pair['filename']})

app.layout = html.Div(style={'margin': '0  300px' }, children=[

###############################################################################################
## GRAPH 1
    dcc.RadioItems(
                id='actual-predicted-select',
                options=[
                    {'label': 'Actual', 'value': 'actual'},
                    {'label': 'Predicted', 'value': 'predicted'}
                ],
                value='actual',
                labelStyle={'display': 'inline-block'}
            ),
    dcc.RadioItems(
                id='avg-total-select',
                options=[
                    {'label': 'Average', 'value': 'average'},
                    {'label': 'Total', 'value': 'total'}
                ],
                value='average',
                labelStyle={'display': 'inline-block'}
            ),
    dcc.RadioItems(
                id='time-select',
                options=[
                    {'label': 'Hourly', 'value': 'hourly'},
                    {'label': 'Daily', 'value': 'daily'},
                    {'label': 'Weekly', 'value': 'weekly'},
                    {'label': 'Monthly', 'value': 'monthly'}
                ],
                value='weekly',
                labelStyle={'display': 'inline-block'}
            ),
    dcc.Dropdown(
        id='building-names',
        options=locations,
        value=filenames_labels[0]['filename'],
        multi=True
    ),

    html.Div(id='actual-graph-container', children=[
        dcc.Graph(
        )
    ]),

###############################################################################################
## GRAPH 2
    dcc.DatePickerRange(
        id='my-date-picker-range',
        min_date_allowed=date(2020, 1, 1),
        max_date_allowed=date(2020, 9, 19),
        initial_visible_month=date(2020, 1, 5),
        end_date=date(2017, 8, 25)
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
])


@app.callback([
    dash.dependencies.Output('building-names', 'multi'),
    dash.dependencies.Output('building-names', 'value')],
    [dash.dependencies.Input('actual-predicted-select', 'value'),
     dash.dependencies.State('building-names', 'value')])
def update_output(actual_predicted, building_names):
    multi = True
    if actual_predicted == 'predicted':
        if (isinstance(building_names, str)):
            building_names = [building_names]
        building = building_names[0]
        multi = False
    else:
        building = building_names

    return multi, building


@app.callback(
    dash.dependencies.Output('actual-graph-container', 'children'),
    [dash.dependencies.Input('building-names', 'value'),
     dash.dependencies.Input('time-select', 'value'),
     dash.dependencies.Input('avg-total-select', 'value'),
     dash.dependencies.Input('actual-predicted-select', 'value')])
def update_output(filenames, time_select, avg_total, actual_predicted):
    """
    This callback fires when the building-names dropdown, and time period
    selection fields are changed in the view
    :param filenames: names of files to be rendered into graphs
    :param labels: labels associated with filename
    :param time_select: hourly, daily, weekly, monthly
    :return: a single of multi-line graph based on the inputs
    """
    is_predicted = False
    if actual_predicted == 'predicted':
        is_predicted = True

    graph = ActualPlot.build_graph(filenames, time_select, avg_total, is_predicted)
    return graph

@app.callback(
    dash.dependencies.Output('predictive-graph-container', 'children'),
    [dash.dependencies.Input('building-names', 'value'),
     dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date'),
     dash.dependencies.Input('time-select-pred', 'value')])
def update_output(filenames, start_date, end_date, time_select_pred):
    string_prefix = 'You have selected: '
    
    predictive_graph = PredictivePlot(filenames)

    if start_date is not None:
        start_date_object = date.fromisoformat(start_date)
        start_date_string = start_date_object.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'Start Date: ' + start_date_string + ' | '
    if end_date is not None:
        end_date_object = date.fromisoformat(end_date)
        end_date_string = end_date_object.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'End Date: ' + end_date_string
    if start_date is not None and end_date is not None:
        graph = predictive_graph.create_graph(start_date_string, end_date_string, time_select_pred)
        return graph

if __name__ == '__main__':
    app.run_server(debug=True)
