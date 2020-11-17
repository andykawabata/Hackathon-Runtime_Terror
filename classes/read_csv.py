import os
import glob
import pandas as pd

"""
Data class gives access to all data in the data/Analysis folder.
Data stored in .csv format and is accessable through dataframes.
"""
class Data:
    def __init__(self):
        self.path = "data/Analysis/*.csv"
    
    # Return all file names from data folder
    def get_all_file_names(self):
        file_names = []
        for file in glob.glob(self.path):
            file_names.append(os.path.basename(file))
        return file_names

    # Return dataframes for specific list of files
    def get_dfs_for_files(self, file_names):
        dfs = []
        for file in glob.glob(self.path):
            file_local = file.split("\\")[-1]
            if file_local in file_names:
                df = pd.read_csv(file)
                dfs.append(df)
        return dfs

    # Return dataframes for all files in data folder
    def get_dfs_for_all_files(self):
        dfs = []
        for file in glob.glob(self.path):
            df = pd.read_csv(file)
            dfs.append(df)
        return dfs


