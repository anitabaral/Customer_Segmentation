import datetime as dt

import pandas as pd

from .load_data import LoadPreprocess


class RFMData:
    def __init__(self, path):
        self.preprocessed_data = LoadPreprocess(path).cleaned_data()

    def get_rfm_data(self):
        today = dt.datetime(2012, 1, 9)
        data_monetary_recency = self.preprocessed_data.groupby("customer_id").agg(
            {
                "spend_amount": lambda x: x.sum(),
                "invoice_date": lambda x: (today - x.max()).days,
            }
        )
        data_temp = self.preprocessed_data.groupby(["customer_id", "invoice_num"]).agg(
            {"spend_amount": lambda x: x.sum()}
        )
        data_frequency = data_temp.groupby("customer_id").agg(
            {"spend_amount": lambda x: len(x)}
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
