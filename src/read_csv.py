import pandas as pd
import os
import numpy as np
from datetime import datetime

# from src.folderObserver import FolderObserver

# if __name__ == "__main__":
#     watch = FolderObserver()
#     watch.launch()


data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'kemi_raw.csv'))
headers = ["char", "time", "c_1", "c_2",
           'point_0', "point_1", "point_2", "point_3", "point_4", "point_5",
           "point_6", 'point_7', 'point_8', 'point_9', 'point_10', 'point_11',
           'point_12', 'point_13', 'point_14', 'point_15', 'point_16', 'point_17']

if __name__ == "__main__":
    print("reading csv: ", data_path)
    data = pd.DataFrame(pd.read_csv(data_path, names=headers))
    data['time'] = pd.to_datetime(data['time']).values.astype(np.int64)
    means = pd.DataFrame(data['time'])
    for i in range(3):
        test = data.iloc[:, 4 + 6 * i:4 + 6 * (i + 1)].mean(axis=1)
        means = pd.concat([means, test], axis=1)
    means.set_index('time', inplace=True)
    print(means)
