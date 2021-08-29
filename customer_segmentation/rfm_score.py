import pandas as pd

from .rfm_values import RFMData


class RFMScore:
    def __init__(self, path):

        self.data_rfm = RFMData(path).get_rfm_data()
        self.quantiles = self.data_rfm[["recency", "frequency", "monetary"]].quantile(
            q=[0.20, 0.40, 0.60, 0.80]
        )

    def r_score(self, r, values):

        if r < self.quantiles[values][0.20]:
            return 5
        elif r < self.quantiles[values][0.40]:
            return 4
        elif r < self.quantiles[values][0.60]:
            return 3
        elif r < self.quantiles[values][0.80]:
            return 2
        else:
            return 1

    def fm_score(self, r, values):

        if r > self.quantiles[values][0.80]:
            return 5
        elif r > self.quantiles[values][0.60]:
            return 4
        elif r > self.quantiles[values][0.40]:
            return 3
        elif r > self.quantiles[values][0.20]:
            return 2
        else:
            return 1

    def combine_scores(self):

        rfm_df_score = self.data_rfm.copy()
        rfm_df_score["r_score"] = rfm_df_score.recency.apply(
            lambda x: self.r_score(x, "recency")
        )
        rfm_df_score["f_score"] = rfm_df_score.frequency.apply(
            lambda x: self.fm_score(x, "frequency")
        )
        rfm_df_score["m_score"] = rfm_df_score.monetary.apply(
            lambda x: self.fm_score(x, "monetary")
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
