import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

class GraphOneComponents:

    @staticmethod
    def radio_actual_pred():
        radios = dcc.RadioItems(
                            id='actual-predicted-select',
                            options=[
                                {'label': 'Actual', 'value': 'actual'},
                                {'label': 'Predicted', 'value': 'predicted'}
                            ],
                            value='actual',
                            labelStyle={'display': 'inline-block',
                                        'padding': '4px 12px 3px 5px',
                                        'font-size': '.9rem'},
                            inputStyle={'margin-right': '4px'}
                        )
        return radios

    @staticmethod
    def radio_avg_total():
        radios = dcc.RadioItems(
            id='avg-total-select',
            options=[
                {'label': 'Average', 'value': 'average'},
                {'label': 'Total', 'value': 'total'}
            ],
            value='average',
            labelStyle={'display': 'inline-block',
                        'padding': '4px 12px 3px 5px',
                        'font-size': '.9rem'},
            inputStyle={'margin-right': '4px'}
        )
        return radios

    @staticmethod
    def radio_time():
        radios = dcc.RadioItems(
            id='time-select',
            options=[
                {'label': 'Hourly', 'value': 'hourly'},
                {'label': 'Daily', 'value': 'daily'},
                {'label': 'Weekly', 'value': 'weekly'},
                {'label': 'Monthly', 'value': 'monthly'}
            ],
            value='weekly',
            labelStyle={'display': 'inline-block',
                        'padding': '4px 12px 3px 5px',
                        'font-size': '.9rem'},
            inputStyle={'margin-right': '4px'}
        )
        return radios

    @staticmethod
    def aggregate_type_tooltip():
        desc = "The aggregate function will switch the graph between the average and total energy consumption for the selected time period."
        tt = dbc.Tooltip(
            desc,
            target='aggregate-select'
        )
        return tt

    @staticmethod
    def timeframe_tooltip():
        tt = dbc.Tooltip(
            "Select a timeframe to view detailed corresponding data.",
            target="timeframe-select",
        )
        return tt

    @staticmethod
    def value_type_tooltip():
        tt = dbc.Tooltip(
            "View the actual or the predicted data.",
            target="value-type",
        )
        return tt

    @staticmethod
    def drop_down_tooltip():
        tt = dbc.Tooltip(
            "Select one or more buildings to view their average energy consumption. Note, you can't select multiple if values type is set to predicted.",
            target="graph-1-dd",
        )
        return tt

    @staticmethod
    def graph_tooltip():
        tt = dbc.Tooltip(
            "Hover over the graph to view the average and predicted energy usage valeus for the selected timeframe.",
            target="predictive-graph-container",
        )
        return tt
