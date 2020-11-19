from classes.read_csv import Data
import pandas as pd

reader = Data()
files = reader.get_all_file_names()
base_path = './data/Analysis/'
avgs = []
for file in files:
    data = pd.read_csv(base_path + file)
    row = data.iloc[-24:, 0]
    avgs.append(row.mean())
print(avgs)