import pandas as pd

from data_processing.label_mapper import LabelMapper

class GroupDataMultiple:

    def __init__(self):
        return

    @staticmethod
    def get_hourly(filenames, columns):
        label_map = LabelMapper.map_to_dictionary()
        base_path = './data/Analysis/'
        merged = pd.DataFrame()
        columns.append('Datetime')
        # merge given files and columns into a single data frame
        for i in range(0, len(filenames)):
            df = pd.read_csv(base_path + filenames[i])
            df = df[columns]
            for index, column in enumerate(columns):
                # create string to append after building name
                string_to_append = ' - ' + column if len(columns) > 2 else ''
                if column != 'Datetime':
                    df = df.rename(columns={columns[index]: label_map[filenames[i]] + string_to_append})
            if merged.empty:
                merged = df
                continue
            merged = pd.merge(merged, df, on="Datetime")
        merged = merged.rename(columns={'Datetime': 'Hour'})
        merged = merged.set_index('Hour')
        return merged

    @staticmethod
    def get_daily(filenames, is_total, columns):
        label_map = LabelMapper.map_to_dictionary()
        merged = pd.DataFrame()
        base_path = './data/Analysis/'
        columns.append('Datetime')
        # merge given files and columns into a single data frame
        for i in range(0, len(filenames)):
            df = pd.read_csv(base_path + filenames[i])
            df = df[columns]
            # rename columns to the building name + the category
            for index, column in enumerate(columns):
                # create string to append after building name
                string_to_append = ' - ' + column if len(columns) > 2 else ''
                if column != 'Datetime':
                    df = df.rename(columns={columns[index]: label_map[filenames[i]] + string_to_append})
            if merged.empty:
                merged = df
                continue
            merged = pd.merge(merged, df, on="Datetime")

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
    def get_weekly(filenames, is_total, columns):
        label_map = LabelMapper.map_to_dictionary()
        merged = pd.DataFrame()
        base_path = './data/Analysis/'
        columns.append('Datetime')
        # merge given files and columns into a single data frame
        for i in range(0, len(filenames)):
            df = pd.read_csv(base_path + filenames[i])
            df = df[columns]
            # rename columns to the building name + the category
            for index, column in enumerate(columns):
                # create string to append after building name
                string_to_append = ' - ' + column if len(columns) > 2 else ''
                if column != 'Datetime':
                    df = df.rename(columns={columns[index]: label_map[filenames[i]] + string_to_append})
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
    def get_monthly(filenames, is_total, columns):
        label_map = LabelMapper.map_to_dictionary()
        merged = pd.DataFrame()
        base_path = './data/Analysis/'
        columns.append('Datetime')
        # merge given files and columns into a single data frame
        for i in range(0, len(filenames)):
            df = pd.read_csv(base_path + filenames[i])
            df = df[columns]
            # rename columns to the building name + the category
            for index, column in enumerate(columns):
                # create string to append after building name
                string_to_append = ' - ' + column if len(columns) > 2 else ''
                if column != 'Datetime':
                    df = df.rename(columns={columns[index]: label_map[filenames[i]] + string_to_append})
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
        # merge given files and columns into a single data frame
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


