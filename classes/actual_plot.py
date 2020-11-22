from classes.group_data import GroupData
from classes.group_data_multiple import GroupDataMultiple
import plotly.express as px
import dash_core_components as dcc


class ActualPlot:

    @staticmethod
    def build_graph(filenames, time_select, avg_total, is_predicted):
        is_total = True
        if avg_total == 'average':
            is_total = False
        columns = ['Actual']
        if is_predicted:
            columns.append('Predicted')

        df = None
        if (isinstance(filenames, str)):
            filenames = [filenames]
        if time_select == 'hourly':
            df = GroupDataMultiple.get_hourly(filenames, columns)
        elif time_select == 'daily':
            df = GroupDataMultiple.get_daily(filenames, is_total, columns)
        elif time_select == 'weekly':
            df = GroupDataMultiple.get_weekly(filenames, is_total, columns)
        else:
            df = GroupDataMultiple.get_monthly(filenames, is_total, columns)
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
