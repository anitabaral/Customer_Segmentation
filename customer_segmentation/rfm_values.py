import datetime as dt

import pandas as pd

from .load_data import LoadPreprocess


class RFMData:
    def __init__(self, path: str):
        self.preprocessed_data = LoadPreprocess(path).cleaned_data()

    def __repr__(self) -> pd.DataFrame:
        return "{self.__class__.__name__}({self.preprocessed_data})".format(self=self)

    def get_rfm_data(self):
        """Calculates recency, frequency and monetary values by agrregating spend_amount and invoice_date.

        Returns:
            object:  Dataframe that consists of recency, frequency, monetary, as columns and customer_id as index.
        """
        today = dt.datetime(2012, 1, 9)
        data_monetary_recency = self.preprocessed_data.groupby("customer_id").agg(
            {
                "spend_amount": lambda price: price.sum(),
                "invoice_date": lambda date: (today - date.max()).days,
            }
        )
        data_temp = self.preprocessed_data.groupby(["customer_id", "invoice_num"]).agg(
            {"spend_amount": lambda price: price.sum()}
        )
        data_frequency = data_temp.groupby("customer_id").agg(
            {"spend_amount": lambda price: len(price)}
        )
        data_rfm = pd.merge(data_monetary_recency, data_frequency, on="customer_id")
        data_rfm.rename(
            columns={
                "invoice_date": "recency",
                "spend_amount_y": "frequency",
                "spend_amount_x": "monetary",
            },
            inplace=True,
        )

        return data_rfm
