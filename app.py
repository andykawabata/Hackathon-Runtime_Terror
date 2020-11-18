# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from classes.read_csv import Data
from classes.group_data import group_data

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

reader = Data()
names = reader.get_all_file_names()
labels = [filename.split('_')[0] for filename in names]
locations = []

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
                value='hourly',
                labelStyle={'display': 'inline-block'}
            ),
    html.Div(id='dd-output-container', children=[]),
    dcc.Dropdown(
        id='building-names',
        options=locations,
        value=names[0],
        multi=True
    )
])

@app.callback(
    dash.dependencies.Output('dd-output-container', 'children'),
    [dash.dependencies.Input('building-names', 'value'),
     dash.dependencies.Input('time-select', 'value')])
def update_output(filenames, time_select):
    #THIS FUNCTION IS CALLED WHEN THE SELECTION BOX INPUT CHANGES
    df = None
    if(isinstance(filenames,str)):
        filenames=[filenames]
    if time_select == 'hourly':
        df = group_data.get_hourly(filenames, True)
    if time_select == 'daily':
        df = group_data.get_hourly(filenames, True)
    if time_select == 'weekly':
        df = group_data.get_hourly(filenames, True)
    if time_select == 'monthly':
        df = group_data.get_hourly(filenames, True)
    fig = px.line(df)
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label="1m",
                         step="month",
                         stepmode="backward"),
                    dict(count=6,
                         label="6m",
                         step="month",
                         stepmode="backward"),
                    dict(count=1,
                         label="YTD",
                         step="year",
                         stepmode="todate"),
                    dict(count=1,
                         label="1y",
                         step="year",
                         stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    graph = dcc.Graph(
        figure=fig
    )
    return graph


if __name__ == '__main__':
    app.run_server(debug=True)
