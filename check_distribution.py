import os

import numpy as np
import pandas as pd
import scipy.stats
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
from fitter import Fitter
import fitter
from scipy.stats import kstest

matplotlib.use('QT5Agg')


def get_normal_distribution(mean: float, sigma: float, amount: int):
    return np.random.normal(mean, sigma, amount)


def get_data_set(filename: str):
    return pd.read_csv(filepath_or_buffer=filename, header=None)


def draw_hist(dataset: pd.DataFrame):
    if isinstance(dataset, pd.DataFrame):
        dataset.hist(bins=100)
    if isinstance(dataset, np.ndarray):
        print("list")
        plt.hist(dataset, 100)


def get_common_distributions():
    return fitter.get_common_distributions() + ["foldcauchy"]


def print_best_and_summary(dataset: pd.DataFrame, distributions=get_common_distributions()):

    f = None
    if isinstance(dataset, pd.DataFrame):
        f = Fitter(dataset.values, distributions=distributions)

    elif isinstance(dataset, np.ndarray):
        f = Fitter(dataset, distributions=distributions)

    f.fit()
    print(f.get_best(method="sumsquare_error"), "\n")
    print(f.summary())


def display():
    plt.show()


def print_filename_and_amount(filename, numbers):
    print("\n")
    print(filename, "\n")
    print(len(numbers), "values")


def prepare_file_before_checking(filename):
    dataset = get_data_set(filename)
    print_filename_and_amount(filename, dataset[0].tolist())
    return dataset


def check_uniformity_for_dataset(dataset):
    dataset.info()
    print(dataset)
    if isinstance(dataset, pd.DataFrame):
        dataset = dataset[0].values.tolist()

    print(kstest(dataset, scipy.stats.uniform(loc=0.1, scale=0.001).cdf))


def check_uniformity_for_file(filename):
    dataset = prepare_file_before_checking(filename)
    check_uniformity_for_dataset(dataset)
    return dataset


def print_parameters_of_file(filename: str, distributions=get_common_distributions()) -> pd.DataFrame:
    dataset = prepare_file_before_checking(filename)
    print_best_and_summary(dataset, distributions)
    return dataset


def print_parameters_for_all_files(distributions=get_common_distributions(), show=True):
    os.chdir("output")
    files = os.listdir()
    files.sort()

    dataset = []
    for file in files:
        if os.stat(file).st_size != 0:
            if distributions == "uniform":
                dataset.append(check_uniformity_for_file(file))
            else:
                dataset.append(print_parameters_of_file(file, distributions))

            # dataset[0].hist(bins=100)

            if show:
                display()

    os.chdir("..")


def check_distributions(show=True):
    print_parameters_for_all_files(get_common_distributions(), show)


if __name__ == "__main__":
    check_distributions()
