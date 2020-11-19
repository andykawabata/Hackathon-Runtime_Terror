from classes.group_data import GroupData
import plotly.express as px
import dash_core_components as dcc


class ActualPlot:

    @staticmethod
    def build_graph(filenames, time_select):
        df = None
        if (isinstance(filenames, str)):
            filenames = [filenames]
        if time_select == 'hourly':
            df = GroupData.get_hourly(filenames)
        elif time_select == 'daily':
            df = GroupData.get_daily(filenames, True)
        elif time_select == 'weekly':
            df = GroupData.get_weekly(filenames, True)
        else:
            df = GroupData.get_hourly(filenames, True)
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
