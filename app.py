# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
from data_processing.read_csv import Data
from chart_builders.predictive_plot import PredictivePlot
from chart_builders.actual_plot import ActualPlot
from data_processing.label_mapper import LabelMapper
from chart_builders import InteractiveMap
import dash_bootstrap_components as dbc
from layout.graph_one_components import GraphOneComponents
from layout.graph_two_components import  GraphTwoComponents

style1 = 'https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css'
style2 = 'styles/style.css'

external_stylesheets = [style1, style2]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

filenames_labels = LabelMapper.map_to_array()
locations = []
files = Data().get_all_file_names()

# BUILD LABELS AND VALUES FOR BUILDING SELECTION DROPDOWN
for pair in filenames_labels:
    locations.append({'label': pair['label'], 'value': pair['filename']})

# Navigation bar
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("True Data Graph", href="#/actual-graph")),
        dbc.NavItem(dbc.NavLink("Average Data Graph", href="predicted-graph")),
        dbc.NavItem(dbc.NavLink("Map", href="#")),
    ],
    brand="UNCG Energy Dashboard",
    brand_href="actual-graph",
    color="#0b1b3f",
    dark=True,
    # style={'position': 'fixed', 'zIndex': 999, 'width': '100%'}
    
)

app.layout = html.Div( children=[
    navbar,
    # Html Definition for Interactive Plotly Graph
    InteractiveMap.return_html_def_building_plot(),
    dbc.Container([
        ###############################################################################################
        ## GRAPH 1
        html.Span([
            html.H3('Energy Consuption by Location', 
            className='mt-2', id='actual-graph'
            )
        ]),
        # html.H3('Energy Consuption at UNCG by Location', className='mt-2', id='actual-graph'),
        html.H6('Further description of graph.'),
        dbc.Row([
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        html.H6('Aggregate Type'),
                        GraphOneComponents.radio_avg_total(),
                        ],
                    ),
                    className="mb-3",
                ),
                md=3

             ),
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        html.H6('Time Frame'),
                        GraphOneComponents.radio_time()
                        ],
                        # style={'padding': '12px'}
                    ),
                    className="mb-3",

                ),
                md=5
            ),
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        html.H6('Value Type'),
                        GraphOneComponents.radio_actual_pred(),
                        ],
                        # style={'padding': '12px'}
                    ),
                    className="mb-3",
                ),
                md=4
            ),
        ]),
        dbc.Row([
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        html.H5('Select Location'),
                        html.P('Choose multiple locations to compare trends.',
                               id='select-desc-multi'),
                        html.P('Choose a location to compare actual and predicted trends.',
                               id='select-desc-single',
                               ),
                        dcc.Dropdown(
                            id='building-names',
                            options=locations,
                            value=filenames_labels[0]['filename'],
                            multi=True,
                        )
                    ]),
                    style={'height': '80%'},
                ),
                md=3
            ),
            dbc.Col(
                html.Div(id='actual-graph-container', children=[
                    dcc.Graph(
                    )
                ]),
                md=9
            )
        ]),



        ###############################################################################################
        ## GRAPH 2
        html.Span([
            html.H3('Average Energy Consuption by Location', 
            className='mt-2', id='predicted-graph',
            ),
        ]),
        html.H6('Further description of graph.'),

        dbc.Row([
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        html.H6('Time Frame'),
                        GraphTwoComponents.radio_pred(),
                        GraphTwoComponents.tf_tooltip()
                    ],
                        style={'padding': '12px'}
                    ),
                    className="mb-3",
                    id='timeframe-graph2'

                ),
                md=4
            ),
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        html.H6('Description'),
                        GraphTwoComponents.pred_graph_description(),
                        
                        GraphTwoComponents.desc_tooltip()
                    ],
                    style={'padding': '12px'}
                    ),
                    className="mb-3",
                    style={'padding': '12px'},
                    id='description-graph2'
                ),
                md=8,
                width = 18,
            )
        ]),

        dbc.Row([
            dbc.Col(
                dbc.Card(
                        dbc.CardBody([
                            html.H5('Select Location'),
                            html.P('Choose a location to view the average erergy usage.'),
                            #    id='select-multi'),
                            html.P('Each location contains actual and predicted data.',
                                   #    id='select-multi2',
                                   ),
                            dcc.Dropdown(
                                id='building-names-pred',
                                options=locations,
                                value=filenames_labels[0]['filename'],
                                multi=False,
                            )
                        ]),
                        style={'height': '80%'},
                    ),
                    
                md=3
            ),
            dbc.Col(
                html.Div(id='predictive-graph-container', children=[
                    dcc.Graph(
                    )
                ]),
                md=9
            )
        ]),
    ])
],
id='body'
)


@app.callback([
    dash.dependencies.Output('building-names', 'multi'),
    dash.dependencies.Output('building-names', 'value'),
    dash.dependencies.Output('select-desc-multi', 'style'),
    dash.dependencies.Output('select-desc-single', 'style')],
    [dash.dependencies.Input('actual-predicted-select', 'value'),
     dash.dependencies.State('building-names', 'value'),
     ])
def update_output(actual_predicted, building_names):
    multi = True
    visible = {'display': 'block'}
    invisible = {'display': 'none'}
    multi_desc = invisible
    single_desc = invisible
    if actual_predicted == 'predicted':
        if (isinstance(building_names, str)):
            building_names = [building_names]
        building = building_names[0]
        multi = False
        single_desc = visible
    else:
        building = building_names
        multi_desc = visible

    return multi, building, multi_desc, single_desc


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
    if len(filenames) == 0:
        return dcc.Graph()
    is_predicted = False
    if actual_predicted == 'predicted':
        is_predicted = True

    graph = ActualPlot.build_graph(filenames, time_select, avg_total, is_predicted)
    return graph

@app.callback(
    dash.dependencies.Output('predictive-graph-container', 'children'),
    [dash.dependencies.Input('building-names-pred', 'value'),
     dash.dependencies.Input('time-select-pred', 'value')])
def update_output(filename, time_select_pred):
    """
    This callback fires when the building-names-pred dropdown, and time period
    selection fields are changed in the view
    :param filename: name of file to be rendered into prediction graph
    :param labels: labels associated with filename
    :param time_select_pred: hourly, daily, weekly, monthly
    :return: a multi-line graph based on the inputs
    """
    predictive_graph = PredictivePlot(filename[0])
    graph = predictive_graph.create_graph2(Data().get_df_for_file(filename), time_select_pred)
    return graph

if __name__ == '__main__':
    app.run_server(debug=True)
