import pandas as pd

from data_processing.label_mapper import LabelMapper

class GroupData:

    def __init__(self):
        return

    @staticmethod
    def get_hourly(filenames, column):
        label_map = LabelMapper.map_to_dictionary()
        base_path = './data/Analysis/'
        merged = pd.DataFrame()
        for i in range(0, len(filenames)):
            df = pd.read_csv(base_path + filenames[i])
            df = df[['Datetime', column]]
            df = df.rename(columns={column: label_map[filenames[i]]})
            if merged.empty:
                merged = df
                continue
            merged = pd.merge(merged, df, on="Datetime")
        merged = merged.set_index('Datetime')
        return merged

    @staticmethod
    def get_daily(filenames, is_total, column):
        label_map = LabelMapper.map_to_dictionary()
        merged = pd.DataFrame()
        base_path = './data/Analysis/'
        for i in range(0, len(filenames)):
            df = pd.read_csv(base_path + filenames[i])
            df = df[['Datetime', column]]
            df = df.rename(columns={column: label_map[filenames[i]]})
            if merged.empty:
                merged = df
                continue
            merged = pd.merge(merged, df, on="Datetime")
        # Adding a Day column and grouping the data by day
        merged['Datetime'] = merged['Datetime'].apply(lambda x: x[:19])
        merged['Datetime'] = pd.to_datetime(merged['Datetime'], errors='coerce')
        merged['Day'] = merged['Datetime'].dt.to_period("D")
        grouped = merged.groupby('Day')
        if is_total:
            daily = grouped.sum()
        else:
            daily = grouped.mean()
        daily.index = daily.index.astype('str')
        return daily

    @staticmethod
    def get_weekly(filenames, is_total, column):
        merged = pd.DataFrame()
        base_path = './data/Analysis/'
        for i in range(0, len(filenames)):
            df = pd.read_csv(base_path + filenames[i])
            df = df[['Datetime', column]]
            df = df.rename(columns={column: filenames[i]})
            if merged.empty:
                merged = df
                continue
            merged = pd.merge(merged, df, on="Datetime")
        # Adding a Week column and grouping the data by week
        merged['Datetime'] = merged['Datetime'].apply(lambda x: x[:19])
        merged['Datetime'] = pd.to_datetime(merged['Datetime'], errors='coerce')
        merged['Week'] = merged['Datetime'].dt.to_period(freq = 'W').apply(lambda r: r.start_time)
        grouped = merged.groupby('Week')
        if is_total:
            weekly = grouped.sum()
        else:
            weekly = grouped.mean()
        weekly.index = weekly.index.astype('str')
        return weekly

    @staticmethod
    def get_monthly(filenames, is_total, column):
        merged = pd.DataFrame()
        base_path = './data/Analysis/'
        for i in range(0, len(filenames)):
            df = pd.read_csv(base_path + filenames[i])
            df = df[['Datetime', column]]
            df = df.rename(columns={column: filenames[i]})
            if merged.empty:
                merged = df
                continue
            merged = pd.merge(merged, df, on="Datetime")
        # Adding a Month column and grouping the data by Month
        merged['Datetime'] = merged['Datetime'].apply(lambda x: x[:19])
        merged['Datetime'] = pd.to_datetime(merged['Datetime'], errors='coerce')
        merged['Month'] = merged['Datetime'].dt.to_period(freq = 'M').apply(lambda r: r.start_time)
        grouped = merged.groupby('Month')
        if is_total:
            monthly = grouped.sum()
        else:
            monthly = grouped.mean()
        monthly.index = monthly.index.astype('str')
        return monthly

    @staticmethod
    def get_yearly(filenames, is_total, column):
        merged = pd.DataFrame()
        base_path = './data/Analysis/'
        for i in range(0, len(filenames)):
            df = pd.read_csv(base_path + filenames[i])
            df = df[['Datetime', column]]
            df = df.rename(columns={column: filenames[i]})
            if merged.empty:
                merged = df
                continue
            merged = pd.merge(merged, df, on="Datetime")
        # Adding a Year column and grouping the data by year
        merged['Datetime'] = merged['Datetime'].apply(lambda x: x[:19])
        merged['Datetime'] = pd.to_datetime(merged['Datetime'], errors='coerce')
        merged['Year'] = merged['Datetime'].dt.to_period(freq = 'Y').apply(lambda r: r.start_time)
        grouped = merged.groupby('Year')
        if is_total:
            yearly = grouped.sum()
        else:
            yearly = grouped.mean()
        yearly.index = yearly.index.astype('str')
        return yearly


