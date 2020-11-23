
import dash
import dash_core_components as dcc
from dateutil import rrule, parser
import dash_html_components as html
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from data_processing.read_csv import Data
from data_processing.group_data import GroupData
import datetime

""" Predictive graph shows average usage and average predicted usage """
class PredictivePlot:
    day_dict = {'Sunday': 0, 'Monday': 1, 'Tuesday': 2, 'Wednesday': 3,
                'Thursday': 4, 'Friday': 5, 'Saturday': 6}

    month_dict = {'January':0, 'February':1, 'March':2, 'April':3, 'May':4,
                  'June':5, 'July':6, 'August': 7, 'September': 8, 'October':9,
                  'November': 10, 'December': 11}

    def __init__(self, filename):
        """Initialize variables and data 
        
        Keywork arguments:
        filename -- the filename of csv data to display in the graph
        """

        self.filename = filename
        self.reader = Data()
        self.names = self.reader.get_all_file_names()
        self.dfs = self.reader.get_df_for_file(filename)
        self.labels = [filename.split('_')[0] for filename in self.names]

    def create_graph2(self, filtered_df, timeframe='Hour'):

            """ Create graph using sub_plots

            Keywork arguments:
            filename -- the filename of csv data to display in the graph
            timeframe -- the amount of time you want to display
            """

            # new_df = df
            mask  = (filtered_df['Datetime'] > '2020-01-01')
            filtered_df = filtered_df.loc[mask]

            # Create filtered df showing only 2020 and up
            dtime = pd.DataFrame(filtered_df)
            filtered_df['Datetime'] = pd.to_datetime(filtered_df.Datetime, errors='coerce', utc=True)
            new_avg_df = pd.DataFrame()

            # Determine the timeframe to display
            if timeframe == 'Hour':
                tf_abbv = "H"
                filtered_df['hour'] = filtered_df['Datetime'].dt.time
                new_avg_df = filtered_df.groupby('hour').mean()
            elif timeframe == 'Day':
                tf_abbv = "D"
                filtered_df['day'] = filtered_df['Datetime'].dt.day_name()
                new_avg_df = filtered_df.groupby('day').mean()
                new_avg_df['day_copy'] = new_avg_df.index
                new_avg_df = new_avg_df.sort_values(by='day_copy', key=lambda x: x.map(self.day_dict))
            elif timeframe == 'Week':
                tf_abbv = "W"
                new_avg_df = filtered_df.groupby(filtered_df['Datetime'].dt.week).mean()
            elif timeframe == 'Month':
                tf_abbv = "M"
                filtered_df['month'] = filtered_df['Datetime'].dt.month_name()
                new_avg_df = filtered_df.groupby('month').mean()
                new_avg_df['month_copy'] = new_avg_df.index
                new_avg_df = new_avg_df.sort_values(by='month_copy', key=lambda x: x.map(self.month_dict))
            else:
                raise ValueError('invalid timeframe input')

            # Create the figure
            fig = go.Figure()
            fig.add_trace(go.Scatter(x = new_avg_df.index,
                                     y = new_avg_df['Actual'],
                                     name = "Actual",)
                          )
            fig.add_trace(go.Scatter(x = new_avg_df.index,
                                     y = new_avg_df['Predicted'],
                                     mode = "markers",
                                     name = "Predicted",
                                     )
                          )
            fig.update_layout(hovermode='x unified')
            fig.update_layout(title="Average Energy Usage for each {} in 2020.".format(timeframe))
            fig.update_xaxes(title_text=timeframe)
            fig.update_yaxes(title_text='Energy Usage')
            predictive = dcc.Graph(
                id='example-graph',
                figure=fig
            )
            return predictive
