from customer_segmentation import CustomerDivisions


def test_get_individual_segments():
    """Testing whether or not the dataframe contains only one rfm segment"""
    customerDivisions = CustomerDivisions("dataset/cleaned_data.csv")
    input = "Champions"
    customerDivisions.customer_segments()
    output = customerDivisions.get_individual_segments(input)
    assert output.groupby(["segments"]).count().iloc[0].name == "Champions"
    assert output.groupby(["segments"]).count()["monetary"].values[0] == (
        len(output.index)
    )
