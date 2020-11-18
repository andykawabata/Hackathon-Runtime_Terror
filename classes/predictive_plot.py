
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from classes.read_csv import Data

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

    def get_avg_for_timeframe(self, column, df, timeframe=1):
        """ Get average values for given timeframe.
        
        Keyword arguments:
        timeframe -- 1: 1 hour, 2: 1 day, 3: 1 week, 4: 1 month, 5: 1 year
        column -- the column of the dataframe, i.e. 'Predicted' or 'Actual'
        df -- the dataframe to collect data for average calculations
        """

        df_new = pd.DataFrame()
        for index, row in enumerate(df[column], start=1):
            if index % timeframe == 0:
                pass

    def create_graph(self, filename=None):
        """ Create graph using sub_plots 
        
        Keywork arguments:
        filename -- the filename of csv data to display in the graph
        """

        # Testing:
        print(filename)
        print(self.filename)

        # Clear unnecessary text from dataframe name
        for index, name in enumerate(self.labels):
            self.dfs[index].name = name

        # Use data from new filename if provided
        if filename is not None:
            df = self.reader.get_df_for_file([filename])
            df.name = filename
        else:
            df = self.reader.get_df_for_file([self.filename])
            df.name = filename

        # Create line figure using given dataframe
        fig = px.line(df, x='Datetime', y=['Predicted'])
        lines = []

        # Two subplots to show each line, avg actual and avg predicted
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True,vertical_spacing=0.009,horizontal_spacing=0.009)
        fig['layout']['margin'] = {'l': 50, 'r': 50, 'b': 100, 't': 100}

        fig.append_trace({'x':df['Datetime'], 'y':df['Actual'], 'type':'scatter', 'name':'Actual'},1,1)
        fig.append_trace({'x':df['Datetime'], 'y':df['Predicted'], 'type':'scatter', 'name':'Predicted'},1,1)

        # Add range slider
        fig.update_layout(
            title=df.name,
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

