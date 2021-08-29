from .rfm_score import RFMScore


class CustomerDivisions:
    def __init__(self, path):
        self.rfm_df_score = RFMScore(path).combine_scores()

    def __repr__(self):
        return "{self.__class__.__name__}({self.rfm_df_score})".format(self=self)

    def customer_segments(self):

        seg_map = {
            r"[4-5][4-5]": "Champions",
            r"[3-4][4-5]": "Loyal Customers",
            r"[4-5][2-3]": "Potential Loyalists",
            r"[3-4][0-1]": "Promising",
            r"[1-2]5": "Can't loose",
            r"[1-3][1-4]": "At risk",
            r"[4-5][0-1]": "New Customers",
        }
        self.rfm_df_score["segments"] = self.rfm_df_score["rf_score"].replace(
            seg_map, regex=True
        )

        return self.rfm_df_score
    
    def get_individual_segments(self, segment_name):

        individual_segment = self.rfm_df_score[self.rfm_df_score['segments'] == segment_name]
        return individual_segment

    def get_champions_id_monetary(self, segment):

        self.customer_segments()
        customer_segment_df = self.rfm_df_score[
            self.rfm_df_score["segments"] == segment
        ]
        customer_segment_df["customer_id"] = customer_segment_df.index
        customer_segment_id_monetary = customer_segment_df[
            ["customer_id", "monetary"]
        ].sort_values(by=["monetary"], ascending=False)

        return customer_segment_id_monetary
