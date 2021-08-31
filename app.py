import yaml

from preprocessing import DataCleaning
from customer_segmentation import LoadPreprocess, CustomerDivisions
from visualize_analysis import get_visualizations, rfm_data, RFMVisualizations

with open("config.yaml", "r") as stream:
    file_paths = yaml.safe_load(stream)


if __name__ == "__main__":

    initial_data = LoadPreprocess(file_paths["data_loc"]).load_csv()
    dataCleaning = DataCleaning(initial_data)

    """Deploying in streamlit"""
    cleaned_data = DataCleaning(initial_data).get_cleaned_data()
    country_name, customer_segment = get_visualizations(cleaned_data)
    if country_name is None:
        pass
    else:
        country_specific_data = dataCleaning.get_single_country_data(country_name)
        country_specific_data.to_csv(
            file_paths["cleaned_country_data_loc"], index=False
        )
        country_customer_divisions = CustomerDivisions(
            file_paths["cleaned_country_data_loc"]
        )
        rfm_visualization = RFMVisualizations(
            country_customer_divisions.customer_segments()
        )
        individual_segment = country_customer_divisions.get_individual_segments(
            customer_segment
        )
        rfm_visualization.vis_contents(cleaned_data, individual_segment)
