import dash_core_components as dcc
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


