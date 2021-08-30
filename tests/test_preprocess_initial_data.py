import pandas as pd
from pathlib import Path

from preprocessing import DataCleaning


def load_initial_data():

    path = Path("dataset/data.csv")
    data = pd.read_csv(path, encoding="unicode_escape")
    return data


def get_renamed_dataframe(input):

    dataCleaning = DataCleaning(input)
    dataCleaning.rename_columns()

    return dataCleaning


def test_replace_zero_values():

    input = load_initial_data()
    dataCleaning = get_renamed_dataframe(input)
    output = dataCleaning.replace_zero_vales()

    if output["unit_price"].any(0.0):
        return "All zeros should be replaced by NaN"


def test_replace_nan_with_null():

    input = load_initial_data()
    dataCleaning = get_renamed_dataframe(input)
    output = dataCleaning.replace_nan_with_null()

    if output[output.isin(["nan"])].empty == False:
        return "nan value still exists in the dataframe."
