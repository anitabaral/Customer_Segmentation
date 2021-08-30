import pandas as pd

from .rfm_score import RFMScore


class TopCandidates:
    def __init__(self, path: str):
        self.rfm_df_score = RFMScore(path).combine_scores()

    def __repr__(self):
        return "{self.__class__.__name__}({self.rfm_df_score})".format(self=self)

    def ten_top_money_spenders(self) -> pd.DataFrame:
        """Returns the top ten big spenders among the customers"""
        self.rfm_df_score[self.rfm_df_score["rfm_score"] == "555"].sort_values(
            "monetary", ascending=False
        ).head(10)

        return self.rfm_df_score

    def ten_top_stopping_possibility(self) -> pd.DataFrame:
        """Returns the top ten customers which the company is on the verge of loosing."""
        self.rfm_df_score[self.rfm_df_score["r_score"] <= 2].sort_values(
            "monetary", ascending=True
        ).head(10)

        return self.rfm_df_score

    def ten_lost_customers(self) -> pd.DataFrame:
        """Returns the ten customers which the company lost."""
        self.rfm_df_score[self.rfm_df_score["rfm_score"] == "111"].sort_values(
            "recency", ascending=False
        ).head(10)

        return self.rfm_df_score
