import pytest

import pandas as pd
from pathlib import Path

from preprocessing import DataCleaning


@pytest.fixture
def load_initial_data():

    path = Path("dataset/data.csv")
    data = pd.read_csv(path, encoding="unicode_escape")
    dataCleaning = DataCleaning(data)
    dataCleaning.rename_columns()

    return dataCleaning


def test_replace_zero_values(load_initial_data):
    """Testing whether or not the all the zero values of unit price is replaced with NaN"""
    output = load_initial_data.replace_zero_vales()
    assert output["unit_price"].any(
        0.0
    ), "Zero value for price still exist in the dataset"


def test_replace_nan_with_null(load_initial_data):
    """Testing whether or not all the nan values of dataframe is replaced with NaN"""
    output = load_initial_data.replace_nan_with_null()
    assert (
        output[output.isin(["nan"])].empty == False
    ), "nan values still exist in the dataframe"


def test_add_total_price(load_initial_data):

    output = load_initial_data.add_total_price()
    assert output["spend_amount"].equals(
        output["quantity"] * output["unit_price"]
    ), "Spend amount is indicating the wrong basket price"
