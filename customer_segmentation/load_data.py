from pathlib import Path

import pandas as pd


class LoadPreprocess:
    def __init__(self, path: str):
        self.path = path

    def __repr__(self):
        return "{self.__class__.__name__}({self.path})".format(self=self)

    def load_csv(self) -> pd.DataFrame:
        csv_path = Path(self.path)
        if csv_path.is_file():
            data = pd.read_csv(csv_path, encoding="unicode_escape")
        else:
            raise ValueError("Error while reading the csv file.")

        return data

    def cleaned_data(self) -> pd.DataFrame:
        commerce_data = self.load_csv()
        commerce_data.invoice_date = pd.to_datetime(commerce_data.invoice_date)

        return commerce_data
