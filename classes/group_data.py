import pandas as pd

from classes.label_mapper import LabelMapper

class GroupData:

    def __init__(self):
        return

    @staticmethod
    def get_hourly(filenames):
        label_map = LabelMapper.map_to_dictionary()
        base_path = './data/Analysis/'
        merged = pd.DataFrame()
        for i in range(0, len(filenames)):
            df = pd.read_csv(base_path + filenames[i])
            df = df[['Datetime', 'Actual']]
            df = df.rename(columns={"Actual": label_map[filenames[i]]})
            if merged.empty:
                merged = df
                continue
            merged = pd.merge(merged, df, on="Datetime")
        merged = merged.set_index('Datetime')
        return merged

    @staticmethod
    def get_daily(filenames, is_total):
        label_map = LabelMapper.map_to_dictionary()
        merged = pd.DataFrame()
        base_path = './data/Analysis/'
        for i in range(0, len(filenames)):
            df = pd.read_csv(base_path + filenames[i])
            df = df[['Datetime', 'Actual']]
            df = df.rename(columns={"Actual": label_map[filenames[i]]})
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
    def get_weekly(filenames, is_total):
        # filename: array of strings for example [CurrBldg_results.csv, Graham_results.csv]
        # is_total: boolean specifying if the weekly averages or weekly totals should be calculated
        # returns: Pandas data frame where the index is time and the columns are the 'Actual'
        # energy use value. ideally the name of the column should be the building name.
        return

    @staticmethod
    def get_monthly(filenames, type):
        return



