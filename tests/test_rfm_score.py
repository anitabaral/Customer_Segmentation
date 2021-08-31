from pathlib import Path

from customer_segmentation import RFMScore, RFMData, LoadPreprocess


def test_combine_scores():
    """Testing whether or not the string concatentation of r, f and m score is equal to rfm score

    Returns
    -------
    str
        Value that is returned when the test case fails.
    """
    path = Path("dataset/test_data.csv")
    rfm_values = RFMScore(path)
    rfm_df_score = rfm_values.combine_scores()
    input = (
        rfm_df_score["r_score"].map(str)
        + rfm_df_score["f_score"].map(str)
        + rfm_df_score["m_score"].map(str)
    )
    output = rfm_df_score["rfm_score"]

    if input.equals(output):
        return "Concatenation of rfm scores has some errors"
