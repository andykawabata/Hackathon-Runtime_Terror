import pandas as pd

class group_data:

    @staticmethod
    def get_hourly(filenames, is_total):
        base_path = './data/Analysis/'
        merged = pd.read_csv(base_path + filenames[0])
        merged = merged[['Datetime', 'Actual']]
        merged = merged.rename(columns={"Actual": filenames[0]})
        for i in range(1, len(filenames)):
            df = pd.read_csv(base_path + filenames[i])
            cols = df[['Datetime', 'Actual']]
            cols = cols.rename(columns={"Actual": filenames[i]})
            merged = pd.merge(merged, cols, on="Datetime")
        merged = merged.set_index('Datetime')
        return merged

    @staticmethod
    def get_daily(filenames, is_total):
        return

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



