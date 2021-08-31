from .rfm_score import RFMScore


class TopCandidates:
    def __init__(self, path):
        self.rfm_df_score = RFMScore(path).combine_scores()

    def ten_top_money_spenders(self, top_k=10):

        self.rfm_df_score[self.rfm_df_score["rfm_score"] == "555"].sort_values(
            "monetary", ascending=False
        ).head(top_k)

        return self.rfm_df_score

    def ten_top_stopping_possibility(self, top_k=10):

        self.rfm_df_score[self.rfm_df_score["r_score"] <= 2].sort_values(
            "monetary", ascending=True
        ).head(top_k)

        return self.rfm_df_score

    def ten_lost_customers(self, top_k=10):

        self.rfm_df_score[self.rfm_df_score["rfm_score"] == "111"].sort_values(
            "recency", ascending=False
        ).head(top_k)

        return self.rfm_df_score
