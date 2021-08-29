import yaml
import warnings

warnings.filterwarnings("ignore")
import datetime as dt
from pathlib import Path

import squarify
import matplotlib
import pandas as pd
import seaborn as sns
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
from plotly import graph_objs as go


def rfm_data():
    st.subheader("RFM Analysis")
    st.markdown('Recency Frequency Monetary Analysis')
    with st.sidebar:
        country = st.selectbox(
            "Select Country",
            ("United Kingdom", "Germany", "France", "EIRE", "Spain")
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
    def __init__(self, rfm_df_score):
        self.rfm_df_score = rfm_df_score

    def square_visualization(self, segment_vis):
        cmap = matplotlib.cm.viridis
        mini = min(segment_vis['customer_id'])
        maxi = max(segment_vis['customer_id'])
        norm = matplotlib.colors.Normalize(vmin=mini, vmax=maxi)
        colors = [cmap(norm(value)) for value in segment_vis['customer_id']]
        fig = plt.gcf()
        ax = fig.add_subplot()
        fig.set_size_inches(14, 10)
        squarify.plot(sizes=segment_vis['customer_id'], label=segment_vis.segments, alpha=0.5, color=colors, bar_kwargs={'alpha':.8}, text_kwargs={'fontsize':16})
        plt.title("Recency Frequency and Monetary Segments", fontsize=18)
        plt.axis('off')
        plt.show()
        st.pyplot(fig)

    def vis_contents(self):
        self.rfm_df_score.reset_index(inplace=True)
        segment_vis = self.rfm_df_score.groupby('segments')['customer_id'].nunique().sort_values(ascending=False).reset_index()
        self.square_visualization(segment_vis)

    def show_aggregated_data(self, individual_segment):
        if individual_segment is None:
            st.markdown(f'There are no customers for this segment')
        else:
            mean_count = individual_segment[['recency','frequency','monetary']].agg(['mean', 'count'])
            st.markdown("##")
            st.subheader(individual_segment['segments'].iloc[0])
            st.markdown(f"**1. Total number of champions: {int(mean_count['recency'].loc['count'])}**")
            st.markdown(f"**2. Average amount they spend: {int(mean_count['monetary'].loc['mean'])}**")
            st.markdown(f"**3. Average visit {int(mean_count['frequency'].loc['mean'])} in {int(mean_count['recency'].loc['mean'])} days**")



