
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
        axis_labels = []
        hr = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
        day = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        week = [0,1,2,3]
        month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct']

        if timeframe == 'Hour':
            tf_abbv = "H"
            axis_labels = hr
        elif timeframe == 'Day':
            tf_abbv = "D"
            axis_labels = day
        elif timeframe == 'Week':
            tf_abbv = "W"
            axis_labels = week
        elif timeframe == 'Month':
            tf_abbv = "M"
            axis_labels = month
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
        
    # def get_hourly(self, df):

    def create_graph2(self, start_date='2020-01-01', end_date='2020-09-19', timeframe='Hour'):
            """ Create graph using sub_plots 
            
            Keywork arguments:
            filename -- the filename of csv data to display in the graph
            timeframe -- the amount of time you want to display
            """

            axis_labels = []
            hr = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
            hr1 = ['12am','1am','2am','3am','4am','5am','6am','7am','8am','9am','10am','11am','12pm','1pm','2pm','3pm','4pm','5pm','6pm','7pm','8pm','9pm','10pm', '11pm']
            day = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            week = [0,1,2,3,4]
            month = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October']

            # Get average values
            # avg_df = self.get_avg_for_timeframe(self.dfs[0], timeframe)
            # avg_df.rename({0: "Datetime"}, axis='columns')
            # avg_df.columns = ['Datetime', 'Predicted', 'Actual']  
            # mask  = (avg_df['Datetime'] > start_date) & (avg_df['Datetime'] < end_date)
            # filtered_df = avg_df.loc[mask]

            # avg_df['Datetime'] = avg_df.index

            new_df = self.dfs[0]

            mask  = (new_df['Datetime'] > start_date) & (new_df['Datetime'] < end_date)
            filtered_df = new_df.loc[mask]

            print(filtered_df.head(30))

            dtime = pd.DataFrame(filtered_df)
            filtered_df['Datetime'] = pd.to_datetime(filtered_df['Datetime'])#, errors='coerce'
            # dtime = filtered_df['Datetime']

            # new_avg_df = filtered_df.groupby(filtered_df['Datetime'].dt.hour).mean()
            # new_avg_df['Datetime'] = dtime
            # print(new_avg_df.head(30))

            new_avg_df = []

            if timeframe == 'Hour':
                tf_abbv = "H"
                axis_labels = hr
                # filtered_df['Time'] = filtered_df['Datetime'].hour

                # print(filtered_df.head(25))

                new_avg_df = filtered_df.groupby(filtered_df['Datetime'].dt.hour).mean()

                # filtered_df = filtered_df.groupby(pd.to_datetime(filtered_df['Datetime'], errors='coerce', utc=True).dt.hour).mean()
                # new_avg_df['Datetime'] = dtime['Datetime']
            elif timeframe == 'Day':
                tf_abbv = "D"
                axis_labels = day
                new_avg_df = filtered_df.groupby(filtered_df['Datetime'].dt.day).mean()
                # new_avg_df['Datetime'] = dtime.dt.day
            elif timeframe == 'Week':
                tf_abbv = "W"
                axis_labels = week
                new_avg_df = filtered_df.groupby(filtered_df['Datetime'].dt.week).mean()
                # new_avg_df['Datetime'] = dtime.dt.week
            elif timeframe == 'Month':
                tf_abbv = "M"
                axis_labels = month
                new_avg_df = filtered_df.groupby(filtered_df['Datetime'].dt.month).mean()
                # new_avg_df['Datetime'] = dtime.dt.month

            
            print(filtered_df.head(25))
            print(new_avg_df.head(25))

            new_avg_df['Time'] = new_avg_df.index

            # new_avg_df.Time = pd.to_timedelta(new_avg_df.index + ':00', unit=tf_abbv)
            # new_avg_df.index = new_avg_df.index + new_avg_df.Time
            # new_avg_df = new_avg_df.drop('Time', axis=1)
            # new_avg_df.index.name = 'Date'

            print(new_avg_df.head(25))

            # Create line figure using given dataframe
            fig = px.line(new_avg_df, x=new_avg_df['Time'], y=['Predicted'])
            lines = []

            # Two subplots to show each line, avg actual and avg predicted
            fig = make_subplots(rows=2, cols=1, shared_xaxes=True,vertical_spacing=0.009,horizontal_spacing=0.009)
            fig['layout']['margin'] = {'l': 50, 'r': 50, 'b': 100, 't': 100}

            # Plot data
            fig.append_trace({'x':new_avg_df.index, 'y':new_avg_df['Actual'], 'type':'scatter', 'name':'Actual'},1,1)
            fig.append_trace({'x':new_avg_df.index, 'y':new_avg_df['Predicted'], 'type':'scatter', 'mode':'markers', 'name':'Predicted'},1,1)
            label = 'Average ' + timeframe + ' for 2020 in ' + str(self.filename.split("_")[0])
            fig.update_layout(hovermode='x unified')
            predictive = dcc.Graph(
                id='example-graph',
                figure=fig
            )
            return predictive
