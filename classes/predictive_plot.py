
import dash
import dash_core_components as dcc
from dateutil import rrule, parser
import dash_html_components as html
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from classes.read_csv import Data
from classes.group_data import GroupData
import datetime

""" Predictive graph shows average usage and average predicted usage """
class PredictivePlot:

    def __init__(self, filename):
        """Initialize variables and data 
        
        Keywork arguments:
        filename -- the filename of csv data to display in the graph
        """

        self.filename = filename
        self.reader = Data()
        self.names = self.reader.get_all_file_names()
        self.dfs = self.reader.get_dfs_for_all_files()
        self.labels = [filename.split('_')[0] for filename in self.names]

    def get_avg_for_timeframe(self, df, timeframe='Week'):
        """ Get average values for given timeframe.
        
        Keyword arguments:
        timeframe -- hour, day, week, month
        column -- the column of the dataframe, i.e. 'Predicted' or 'Actual'
        df -- the dataframe to collect data for average calculations
        """

        tf_abbv = ""

        if timeframe == 'Hour':
            tf_abbv = "H"
        elif timeframe == 'Day':
            tf_abbv = "D"
        elif timeframe == 'Week':
            tf_abbv = "W"
        elif timeframe == 'Month':
            tf_abbv = "M"
        else:
            raise ValueError('Hour, Day, Week, Month')

        # Calculate average values for selected timeframe
        df['Datetime'] = df['Datetime'].apply(lambda x: x[:19])
        df['Datetime'] = pd.to_datetime(df['Datetime'], errors='coerce')
        df[timeframe] = df['Datetime'].dt.to_period(freq = tf_abbv).apply(lambda r: r.start_time)
        grouped = df.groupby(timeframe)
        pred_df = grouped[timeframe, 'Predicted'].mean()
        actual_df = grouped[timeframe, 'Actual'].mean()
        merged = pd.merge(pred_df, actual_df, on=pred_df.index)
        return merged
        
    def create_graph(self, start_date, end_date, timeframe):
        """ Create graph using sub_plots 
        
        Keywork arguments:
        filename -- the filename of csv data to display in the graph
        timeframe -- the amount of time you want to display
        """

        # Get average values
        avg_df = self.get_avg_for_timeframe(self.dfs[0], timeframe)
        avg_df.rename({0: "Datetime"}, axis='columns')
        avg_df.columns = ['Datetime', 'Predicted', 'Actual']
        mask  = (avg_df['Datetime'] > start_date) & (avg_df['Datetime'] < end_date)
        filtered_df = avg_df.loc[mask]

        # Create line figure using given dataframe
        fig = px.line(filtered_df, x=filtered_df.index, y=['Predicted'])
        lines = []

        # Two subplots to show each line, avg actual and avg predicted
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True,vertical_spacing=0.009,horizontal_spacing=0.009)
        fig['layout']['margin'] = {'l': 50, 'r': 50, 'b': 100, 't': 100}

        # Plot data
        fig.append_trace({'x':filtered_df['Datetime'], 'y':filtered_df['Actual'], 'type':'scatter', 'name':'Actual'},1,1)
        fig.append_trace({'x':filtered_df['Datetime'], 'y':filtered_df['Predicted'], 'type':'scatter', 'name':'Predicted'},1,1)
        label = 'Average ' + timeframe + ' for 2020 in ' + str(self.filename.split("_")[0])
        fig.update_layout(hovermode='x unified')
        predictive = dcc.Graph(
            id='example-graph',
            figure=fig
        )
        return predictive

