from pathlib import Path

from customer_segmentation import RFMScore


def test_combine_scores():
    """Testing whether or not the string concatentation of r, f and m score is equal to rfm score"""
    path = Path("dataset/test_data.csv")
    rfm_values = RFMScore(path)
    rfm_df_score = rfm_values.combine_scores()
    input = (
        rfm_df_score["r_score"].map(str)
        + rfm_df_score["f_score"].map(str)
        + rfm_df_score["m_score"].map(str)
    )
    output = rfm_df_score["rfm_score"]

    assert input.equals(
        output
    ), "The concatenation of r, f and m didn't give the same value as rfm score"
