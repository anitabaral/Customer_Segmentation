import yaml
import datetime as dt
from pathlib import Path

import squarify
import matplotlib
import pandas as pd
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt


def rfm_data() -> tuple[str, str]:
    """Displays selectbox to let user select the country and rfm segment

    Returns
    -------
    tuple
        Country and segment selected by the user.
    """
    st.subheader("RFM Analysis")
    st.markdown("Recency Frequency Monetary Analysis")
    with st.sidebar:
        country = st.selectbox(
            "Select Country", ("United Kingdom", "Germany", "France", "EIRE", "Spain")
        )
        segment = st.selectbox(
            "Select RFM Segment",
            (
                "Champions",
                "Loyal Customers",
                "Potential Loyalists",
                "Promising",
                "Can't loose",
                "At risk",
                "New Customers",
            ),
        )
    st.subheader(country)
    st.markdown("##")
    return (country, segment)


class RFMVisualizations:
    def __init__(self, rfm_df_score: pd.DataFrame):
        self.rfm_df_score = rfm_df_score

    def square_visualization(self, segment_vis: pd.DataFrame):
        """Visualizing the square plot of customer segments"""
        cmap = matplotlib.cm.viridis
        mini = min(segment_vis["customer_id"])
        maxi = max(segment_vis["customer_id"])
        norm = matplotlib.colors.Normalize(vmin=mini, vmax=maxi)
        colors = [cmap(norm(value)) for value in segment_vis["customer_id"]]
        fig = plt.gcf()
        ax = fig.add_subplot()
        fig.set_size_inches(14, 10)
        squarify.plot(
            sizes=segment_vis["customer_id"],
            label=segment_vis.segments,
            alpha=0.5,
            color=colors,
            bar_kwargs={"alpha": 0.8},
            text_kwargs={"fontsize": 16},
        )
        plt.title("Recency Frequency and Monetary Segments", fontsize=18)
        plt.axis("off")
        plt.show()
        st.pyplot(fig)

        return None

    def show_aggregated_data(self, individual_segment: pd.DataFrame):
        """Visulize the counts of customers, mean of recency, frequency and monetary of each segment of customers for specific nation"""
        if individual_segment is None:
            st.markdown(f"There are no customers for this segment")
        else:
            mean_count = individual_segment[["recency", "frequency", "monetary"]].agg(
                ["mean", "count"]
            )
            st.markdown("##")
            st.subheader(individual_segment["segments"].iloc[0])
            st.markdown("Detail about the customers belonging to the segment.")
            st.markdown(
                f"**1. Total number of customers: {int(mean_count['recency'].loc['count'])}**"
            )
            st.markdown(
                f"**2. Average amount they spend: {int(mean_count['monetary'].loc['mean'])}**"
            )
            st.markdown(
                f"**3. Average visit {int(mean_count['frequency'].loc['mean'])} in {int(mean_count['recency'].loc['mean'])} days**"
            )

        return None

    def show_customer_dataframe(
        self, preprocessed_data: pd.DataFrame, segment: pd.DataFrame
    ):
        """Visualizing the dataframe of customers data for every segment"""
        preprocessed_data.reset_index(drop=True)
        segment.reset_index(inplace=True)
        segments = preprocessed_data.loc[
            preprocessed_data.customer_id.isin(segment.customer_id)
        ]
        grouped_segments = (
            segments.groupby(["customer_id"])
            .first()
            .reset_index()
            .sort_values("spend_amount", ascending=False)
        )
        st.markdown("##")
        st.subheader("Nations individual segments")
        st.markdown("All the customers belonging to the segment of the given nation.")
        with st.sidebar:
            submit = st.selectbox(
                "Select the top candidates option", ("All candidates", "Top Candidates")
            )
        if submit == "Top Candidates":
            st.dataframe(grouped_segments.reset_index(drop=True).iloc[0:10])
        elif submit == "All candidates":
            st.dataframe(grouped_segments.reset_index(drop=True))

        return None

    def vis_contents(self, preprocessed_data: pd.DataFrame, individual_segment: str):
        """Calling the above functions to visualize elements one by one"""
        self.rfm_df_score.reset_index(inplace=True)
        segment_vis = (
            self.rfm_df_score.groupby("segments")["customer_id"]
            .nunique()
            .sort_values(ascending=False)
            .reset_index()
        )
        self.square_visualization(segment_vis)
        self.show_aggregated_data(individual_segment)
        self.show_customer_dataframe(preprocessed_data, individual_segment)

        return None
