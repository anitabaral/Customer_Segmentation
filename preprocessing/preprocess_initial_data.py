from collections import defaultdict

import numpy as np
import pandas as pd

class DataCleaning:
    def __init__(self, data):
        self.commerce_data = data

    def rename_columns(self):

        self.commerce_data.rename(index=str, columns={'InvoiceNo': 'invoice_num',
                              'StockCode' : 'stock_code',
                              'Description' : 'description',
                              'Quantity' : 'quantity',
                              'InvoiceDate' : 'invoice_date',
                              'UnitPrice' : 'unit_price',
                              'CustomerID' : 'customer_id',
                              'Country' : 'country'}, inplace=True)

        return None

    @staticmethod
    def get_attributes_info(data):

        info = defaultdict(list)
        info['Count'], info['dtypes']  = data.count(), data.dtypes.values
        info['Missing_values'] = data.isnull().sum().values
        info['Missing_values_percentage'] = info['Missing_values'] / data.shape[0] * 100
        info['Unique'] = data.nunique()
        attributes_info = pd.DataFrame(info)

        return attributes_info

    def replace_zero_vales(self):

        self.commerce_data.unit_price = commerce_data.unit_price.replace({0.0: np.nan})

        return None

    @staticmethod
    def check_nan_values(data):

        data['description'] = data.description.str.lower()
        nan = data.description.dropna().apply(
            lambda l: np.where("nan" in l, True, False)
        ).value_counts()
        empty_strings = data.customer_id.dropna().apply(
            lambda l: np.where("" == l, True, False)
        ).value_counts()

        return nan, empty_strings

    def replace_nan_with_null(self):

        self.commerce_data.loc[self.commerce_data.description.isnull()==False, "description"] = self.commerce_data.loc[
        self.commerce_data.description.isnull()==False, "description"
        ].apply(lambda l: np.where("nan" in l, None, l))

        return None

    def add_total_price(self):

        self.commerce_data['spend_amount'] = self.commerce_data['quantity'] * self.commerce_data['unit_price']

        return None

    def rearrange_columns(self):
        
        self.commerce_data = self.commerce_data[['invoice_num','invoice_date','stock_code','description','quantity','unit_price', 'spend_amount', 'customer_id','country', ]]

        return None

    def get_cleaned_data(self):

        self.rename_columns()
        self.replace_nan_with_null()
        self.add_total_price()
        self.rearrange_columns()
        return self.commerce_data


    def get_single_country_data(self, country): 
        self.get_cleaned_data()
        print(country)
        country_specific_data = self.commerce_data[self.commerce_data['country'] == country]

        return country_specific_data