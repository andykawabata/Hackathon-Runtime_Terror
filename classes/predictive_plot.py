
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from classes.read_csv import Data
from classes.group_data import GroupData

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

    def get_avg_for_timeframe(self, column, timeframe=1):
        """ Get average values for given timeframe.
        
        Keyword arguments:
        timeframe -- hourly, daily, weekly, monthly, yearly
        column -- the column of the dataframe, i.e. 'Predicted' or 'Actual'
        df -- the dataframe to collect data for average calculations
        """

        if timeframe == 'Hour':
            return GroupData.get_hourly([self.filename],column)
        elif timeframe == 'Day':
            return GroupData.get_daily([self.filename], False, column)
        elif timeframe == 'Week':
            return GroupData.get_weekly([self.filename], False, column)
        elif timeframe == 'Month':
            return GroupData.get_monthly([self.filename], False, column)
        elif timeframe == 'Year':
            return GroupData.get_yearly([self.filename], False, column)
        else:
            raise ValueError('timeframe must be 1, 2, 3, 4, or 5')


    def create_graph(self, timeframe, filename=None):
        """ Create graph using sub_plots 
        
        Keywork arguments:
        filename -- the filename of csv data to display in the graph
        timeframe -- the amount of time you want to display
        """

        # Get average values from group_data class
        df_actual = self.get_avg_for_timeframe('Actual', timeframe)
        df_predicted = self.get_avg_for_timeframe('Predicted', timeframe)

        # Name the columns
        df_actual.columns = ['Actual']
        df_predicted.columns = ['Predicted']
        predic = df_predicted['Predicted']

        # Set df name and create joined df
        df_actual.name = self.filename
        df_actual = df_actual.join(predic)

        # Create line figure using given dataframe
        fig = px.line(df_actual, x=df_actual.index, y=['Predicted'])
        lines = []

        # Two subplots to show each line, avg actual and avg predicted
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True,vertical_spacing=0.009,horizontal_spacing=0.009)
        fig['layout']['margin'] = {'l': 50, 'r': 50, 'b': 100, 't': 100}

        fig.append_trace({'x':df_actual.index, 'y':df_actual['Actual'], 'type':'scatter', 'name':'Actual'},1,1)
        fig.append_trace({'x':df_actual.index, 'y':df_actual['Predicted'], 'type':'scatter', 'name':'Predicted'},1,1)

        # Add range slider
        fig.update_layout(
            title=self.filename,
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                            label="Hour",
                            step="month",
                            stepmode="backward"),
                        dict(count=6,
                            label="Day",
                            step="month",
                            stepmode="backward"),
                        dict(count=1,
                            label="Month",
                            step="year",
                            stepmode="todate"),
                        dict(count=1,
                            label="Year",
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
        fig.update_layout(hovermode='x unified')
        predictive = dcc.Graph(
            id='example-graph',
            figure=fig
        )
        return predictive

