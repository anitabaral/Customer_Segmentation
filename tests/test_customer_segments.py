from customer_segmentation import RFMScore, CustomerDivisions


def test_get_individual_segments():

    customerDivisions = CustomerDivisions("dataset/cleaned_data.csv")
    input = "Champions"
    customerDivisions.customer_segments()
    output = customerDivisions.get_individual_segments(input)

    if output.groupby(["segments"]).count().iloc[0].name == "Champions":
        if output.groupby(["segments"]).count()["monetary"].values[0] == (
            len(output.index)
        ):
            return "The individual segments contains other segments values as well. "
