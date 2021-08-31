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
    """Testing whether or not the all the zero values of unit price is replaced with NaN

    Returns
    -------
    str
        Value that is returned when the test case fails.
    """
    input = load_initial_data()
    dataCleaning = get_renamed_dataframe(input)
    output = dataCleaning.replace_zero_vales()

    if output["unit_price"].any(0.0):
        return "All zeros should be replaced by NaN"


def test_replace_nan_with_null():
    """Testing whether or not all the nan values of dataframe is replaced with NaN

    Returns
    -------
    str
        Value that is returned when the test case fails.
    """
    input = load_initial_data()
    dataCleaning = get_renamed_dataframe(input)
    output = dataCleaning.replace_nan_with_null()

    if output[output.isin(["nan"])].empty == False:
        return "nan value still exists in the dataframe."
