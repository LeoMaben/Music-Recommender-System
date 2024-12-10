"""
@Author: Leonardo Maben
@Date: 1/12/24

"""
import os

import numpy
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA


def aggregate_data(folder_path):
    '''
    Function to concatenate the metadata and save it into one file

    :param folder_path: path to the original metadata
    '''

    aggregated_data = []

    for file in os.listdir(folder_path):
        path = os.path.join(folder_path, file)
        data = pd.read_csv(path)
        aggregated_data.append(data)

    ad_csv = pd.concat(aggregated_data, ignore_index=True)
    print(ad_csv.head())

    ad_csv.to_csv('aggregated_data.csv', index=False)


def main():
    folder_path = '../metadata/'
    aggregate_data(folder_path)


if __name__ == '__main__':
    main()
