from .rfm_score import RFMScore


class TopCandidates:
    def __init__(self, path):
        self.rfm_df_score = RFMScore(path).combine_scores()

    def ten_top_money_spenders(self):

        self.rfm_df_score[self.rfm_df_score["rfm_score"] == "555"].sort_values(
            "monetary", ascending=False
        ).head()

        return self.rfm_df_score

    def ten_top_stopping_possibility(self):

        self.rfm_df_score[self.rfm_df_score["r_score"] <= 2].sort_values(
            "monetary", ascending=True
        ).head(10)

        return self.rfm_df_score

    def ten_lost_customers(self):

        self.rfm_df_score[self.rfm_df_score["rfm_score"] == "111"].sort_values(
            "recency", ascending=False
        ).head(10)

        return self.rfm_df_score
