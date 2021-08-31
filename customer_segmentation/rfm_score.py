import pandas as pd

from .rfm_values import RFMData


class RFMScore:
    def __init__(self, path: str):
        self.data_rfm = RFMData(path).get_rfm_data()
        self.quantiles = self.data_rfm[["recency", "frequency", "monetary"]].quantile(
            q=[0.20, 0.40, 0.60, 0.80]
        )

    def __repr__(self):
        return "{self.__class__.__name__}({self.data_rfm})".format(self=self)

    def r_score(self, recency: int, values: str) -> int:
        """Returns the r-score on the base of quantiles of recency."""
        if recency < self.quantiles[values][0.20]:
            return 5
        elif recency < self.quantiles[values][0.40]:
            return 4
        elif recency < self.quantiles[values][0.60]:
            return 3
        elif recency < self.quantiles[values][0.80]:
            return 2
        else:
            return 1

    def fm_score(self, f: int, values: str) -> int:
        """Returns f and m score on the basis of quantiles of frequency and monetary resepectively."""
        if f > self.quantiles[values][0.80]:
            return 5
        elif f > self.quantiles[values][0.60]:
            return 4
        elif f > self.quantiles[values][0.40]:
            return 3
        elif f > self.quantiles[values][0.20]:
            return 2
        else:
            return 1

    def combine_scores(self) -> pd.DataFrame:
        """Combines r, f, m score as strings to get rfm score.

        Returns
        -------
        pd.DataFrame
            Dataframe that consists of r, f, m, rf and rfm score as columns additional to data_rfm coloumns.
        """
        rfm_df_score = self.data_rfm.copy()
        rfm_df_score["r_score"] = rfm_df_score.recency.apply(
            lambda r: self.r_score(r, "recency")
        )
        rfm_df_score["f_score"] = rfm_df_score.frequency.apply(
            lambda f: self.fm_score(f, "frequency")
        )
        rfm_df_score["m_score"] = rfm_df_score.monetary.apply(
            lambda m: self.fm_score(m, "monetary")
        )
        rfm_df_score["rfm_score"] = (
            rfm_df_score["r_score"].map(str)
            + rfm_df_score["f_score"].map(str)
            + rfm_df_score["m_score"].map(str)
        )
        rfm_df_score["rf_score"] = rfm_df_score["r_score"].map(str) + rfm_df_score[
            "f_score"
        ].map(str)

        return rfm_df_score
