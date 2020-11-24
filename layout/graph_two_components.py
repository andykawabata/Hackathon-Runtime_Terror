import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

class GraphTwoComponents:

    @staticmethod
    def radio_pred():
        radios = dcc.RadioItems(
            id='time-select-pred',
            options=[
                {'label': 'Hourly', 'value': 'Hour'},
                {'label': 'Daily', 'value': 'Day'},
                {'label': 'Weekly', 'value': 'Week'},
                {'label': 'Monthly', 'value': 'Month'}
            ],
            value='Day',
            labelStyle={'display': 'inline-block',
                        'padding': '4px 12px 3px 5px',
                        'font-size': '.9rem'},
            inputStyle={'margin-right': '4px'}
        )
        return radios

    @staticmethod
    def pred_graph_description():
        desc = "This graph displays the mean values of both Actual data and Predicted data. The data displayed represents energy usage for UNCG from 2020-01-01 to present."
        p = html.P(
            desc
        )
        return p

    @staticmethod
    def tf_tooltip():
        tt = dbc.Tooltip(
            "Select to change the timeframe displayed in graph.",
            target="timeframe-graph2",
        )
        return tt

    @staticmethod
    def desc_tooltip():
        tt = dbc.Tooltip(
            "Description of the average value graph.",
            target="description-graph2",
        )
        return tt

    @staticmethod
    def dd_tooltip():
        tt = dbc.Tooltip(
            "Select a building to view its average energy consumption.",
            target="drop-down-graph2",
        )
        return tt

    @staticmethod
    def graph_tooltip():
        tt = dbc.Tooltip(
            "Hover over the graph to view the average and predicted energy usage valeus for the selected timeframe.",
            target="predictive-graph-container",
        )
        return tt

    

