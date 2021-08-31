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
    assert output["unit_price"].any(0.0)


def test_replace_nan_with_null(load_initial_data):
    """Testing whether or not all the nan values of dataframe is replaced with NaN"""

    output = load_initial_data.replace_nan_with_null()
    assert output[output.isin(["nan"])].empty == False
