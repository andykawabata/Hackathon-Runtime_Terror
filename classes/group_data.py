import pandas as pd


class GroupData:

    def __init__(self):
        return

    @staticmethod
    def get_hourly(filenames):
        base_path = './data/Analysis/'
        merged = pd.DataFrame()
        for i in range(0, len(filenames)):
            df = pd.read_csv(base_path + filenames[i])
            df = df[['Datetime', 'Actual']]
            df = df.rename(columns={"Actual": filenames[i]})
            if merged.empty:
                merged = df
                continue
            merged = pd.merge(merged, df, on="Datetime")
        merged = merged.set_index('Datetime')
        return merged

    @staticmethod
    def get_daily(filenames, is_total):
        merged = pd.DataFrame()
        base_path = './data/Analysis/'
        for i in range(0, len(filenames)):
            df = pd.read_csv(base_path + filenames[i])
            df = df[['Datetime', 'Actual']]
            df = df.rename(columns={"Actual": filenames[i]})
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
        merged = pd.DataFrame()
        base_path = './data/Analysis/'
        for i in range(0, len(filenames)):
            df = pd.read_csv(base_path + filenames[i])
            df = df[['Datetime', 'Actual']]
            df = df.rename(columns={"Actual": filenames[i]})
            if merged.empty:
                merged = df
                continue
            merged = pd.merge(merged, df, on="Datetime")

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
    def get_monthly(filenames, type):
        return



