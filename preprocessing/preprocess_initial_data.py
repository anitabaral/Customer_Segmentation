from collections import defaultdict

import numpy as np
import pandas as pd


class DataCleaning:
    def __init__(self, data):
        self.commerce_data = data

    def __repr__(self):
        return "{self.__class__.__name__}({self.commerce_data})".format(self=self)

    def rename_columns(self):
        """Renames the columns for simplicity"""
        self.commerce_data.rename(
            index=str,
            columns={
                "InvoiceNo": "invoice_num",
                "StockCode": "stock_code",
                "Description": "description",
                "Quantity": "quantity",
                "InvoiceDate": "invoice_date",
                "UnitPrice": "unit_price",
                "CustomerID": "customer_id",
                "Country": "country",
            },
            inplace=True,
        )

        return None

    @staticmethod
    def get_attributes_info(data: pd.DataFrame) -> pd.DataFrame:
        """Creates a dataframe with different attributes info.

        Args:
            data (pd.DataFrame): Consist the customers data.

        Returns:
            pd.DataFrame: Dataframe with different attributes info.
        """
        info = defaultdict(list)
        info["count"], info["dtypes"] = data.count(), data.dtypes.values
        info["missing_values"] = data.isnull().sum().values
        info["missing_values_percentage"] = info["missing_values"] / data.shape[0] * 100
        info["unique"] = data.nunique()
        attributes_info = pd.DataFrame(info)

        return attributes_info

    def replace_zero_vales(self) -> pd.DataFrame:
        """Replaces zeros with NaN"""
        self.commerce_data.unit_price.replace({0.0: np.nan}, inplace=True)

        return self.commerce_data

    @staticmethod
    def check_nan_values(data: pd.DataFrame) -> tuple[int, int]:
        """Checks for nan and empty values in the dataframe coloumn description.

        Args:
            data (pd.DataFrame): The customers dataset.

        Returns:
            (int): Number of nan values in the dataframe.
            (int): Number of emptry strings in the dataframe.
        """

        data["description"] = data.description.str.lower()
        nan = (
            data.description.dropna()
            .apply(lambda l: np.where("nan" in l, True, False))
            .value_counts()
        )
        empty_strings = (
            data.customer_id.dropna()
            .apply(lambda l: np.where("" == l, True, False))
            .value_counts()
        )

        return nan, empty_strings

    def replace_nan_with_null(self) -> pd.DataFrame:
        """Returns the dataframe consisting of NaN inplace of nan"""
        self.commerce_data.loc[
            self.commerce_data.description.isnull() == False, "description"
        ] = self.commerce_data.loc[
            self.commerce_data.description.isnull() == False, "description"
        ].apply(
            lambda l: np.where("nan" in l, None, l)
        )

        return self.commerce_data

    def add_total_price(self):
        """Adds new column spend_amount with basket prices for customers"""
        self.commerce_data["spend_amount"] = (
            self.commerce_data["quantity"] * self.commerce_data["unit_price"]
        )

        return None

    def rearrange_columns(self):

        self.commerce_data = self.commerce_data[
            [
                "invoice_num",
                "invoice_date",
                "stock_code",
                "description",
                "quantity",
                "unit_price",
                "spend_amount",
                "customer_id",
                "country",
            ]
        ]

        return None

    def get_cleaned_data(self) -> pd.DataFrame:

        self.rename_columns()
        self.replace_zero_vales()
        self.replace_nan_with_null()
        self.add_total_price()
        self.rearrange_columns()

        return self.commerce_data

    def get_single_country_data(self, country: str) -> pd.DataFrame:
        """Extracts a particular country data as per specified in the country variable.

        Args:
            country (str): Name of the country.

        Returns:
            pd.DataFrame: Specific country data.
        """
        self.get_cleaned_data()
        country_specific_data = self.commerce_data[
            self.commerce_data["country"] == country
        ]

        return country_specific_data
