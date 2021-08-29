import yaml
import warnings

warnings.filterwarnings("ignore")
import datetime as dt
from pathlib import Path

import pandas as pd
import seaborn as sns
import streamlit as st
import plotly.express as px
from matplotlib import rcParams
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
from plotly import graph_objs as go

from .rfm_analysis import rfm_data

rcParams["axes.titlepad"] = 20


class GeographicAnalysis:
    def __init__(self, preprocessed_data):
        self.preprocessed_data = preprocessed_data

    def get_values_per_country(self):

        orders_per_country = (
            self.preprocessed_data.groupby(by=["country"], as_index=False)[
                "invoice_num"
            ]
            .count()
            .sort_values(["invoice_num", "country"], ascending=False)
        )
        orders_per_country.drop([orders_per_country.index[0]], inplace=True)
        customers_per_country = (
            self.preprocessed_data.groupby(by=["country"], as_index=False)[
                "customer_id"
            ]
            .count()
            .sort_values(["customer_id", "country"], ascending=False)
        )
        customers_per_country.drop([customers_per_country.index[0]], inplace=True)
        amount_per_country = (
            self.preprocessed_data.groupby(by=["country"], as_index=False)[
                "spend_amount"
            ]
            .sum()
            .sort_values(["spend_amount", "country"], ascending=False)
        )
        amount_per_country.drop([amount_per_country.index[0]], inplace=True)

        return orders_per_country, customers_per_country, amount_per_country

    @staticmethod
    def bar_plot_vis(
        country_values, x_axis, y_axis, xlabel, ylabel, title, palette_value="Blues_r"
    ):

        f = plt.figure(figsize=(10, 8))
        sns.barplot(
            data=country_values,
            x=country_values[x_axis],
            y=country_values[y_axis],
            palette=palette_value,
            saturation=0.5,
        )
        plt.xlabel(xlabel, fontsize=14)
        plt.ylabel(ylabel, fontsize=14)
        plt.title(title, fontsize=16, pad=20)
        plt.xticks(rotation=90)
        plt.show()
        st.pyplot(f)
        st.markdown("##")

        return None

    def vis_contents(self):

        (
            orders_per_country,
            customers_per_country,
            amount_per_country,
        ) = self.get_values_per_country()
        self.bar_plot_vis(
            orders_per_country,
            "country",
            "invoice_num",
            "Name of the country",
            "No of orders",
            "Number of orders from different countries",
        )
        self.bar_plot_vis(
            customers_per_country,
            "country",
            "customer_id",
            "Name of the country",
            "Number of customers",
            "Number of customers from different countries",
            palette_value="Greens_r",
        )
        self.bar_plot_vis(
            amount_per_country,
            "country",
            "spend_amount",
            "Name of the country",
            "Total amount spent",
            "Total purchases from different countries",
            palette_value="Oranges_r",
        )

        return None


class TimeAnalysis:
    def __init__(self, preprocessed_data):
        self.commerce_data = preprocessed_data
        self.commerce_data.invoice_date = pd.to_datetime(
            self.commerce_data.invoice_date
        )

    def insert_columns(self):

        self.commerce_data.insert(
            loc=2,
            column="year_month",
            value=self.commerce_data["invoice_date"].map(
                lambda x: 100 * x.year + x.month
            ),
        )
        self.commerce_data.insert(
            loc=3, column="month", value=self.commerce_data.invoice_date.dt.month
        )
        self.commerce_data.insert(
            loc=4,
            column="week",
            value=self.commerce_data.invoice_date.apply(lambda x: x.strftime("%W")),
        )
        self.commerce_data.insert(
            loc=5,
            column="day",
            value=(self.commerce_data.invoice_date.dt.dayofweek) + 1,
        )
        self.commerce_data.insert(
            loc=6, column="hour", value=self.commerce_data.invoice_date.dt.hour
        )

        return None

    @staticmethod
    def bar_plot_single_colour(country_values, x_axis, y_axis, xlabel, ylabel, title):

        f = plt.figure(figsize=(10, 8))
        sns.barplot(
            data=country_values,
            x=country_values[x_axis],
            y=country_values[y_axis],
            color="cadetblue",
            saturation=0.5,
        )
        plt.xlabel(xlabel, fontsize=14)
        plt.ylabel(ylabel, fontsize=14)
        plt.title(title, fontsize=16, pad=20)
        plt.xticks(rotation=90)
        plt.show()
        st.pyplot(f)
        st.markdown("##")

        return None

    @staticmethod
    def orders_per_month_vis(orders_per_month):

        f = plt.figure(figsize=(10, 8))
        ax = sns.barplot(
            data=orders_per_month,
            x="year_month",
            y="invoice_num",
            color="cadetblue",
            saturation=0.5,
        )
        ax.set_xlabel("Month", fontsize=14)
        ax.set_ylabel("Number of Orders", fontsize=14)
        ax.set_title(
            "Number of orders for different Months (1st Dec 2010 - 9th Dec 2011)",
            fontsize=15,
            pad=20,
        )
        ax.set_xticklabels(
            (
                "Dec_10",
                "Jan_11",
                "Feb_11",
                "Mar_11",
                "Apr_11",
                "May_11",
                "Jun_11",
                "July_11",
                "Aug_11",
                "Sep_11",
                "Oct_11",
                "Nov_11",
                "Dec_11",
            ),
            rotation="horizontal",
            fontsize=13,
        )
        plt.xticks(rotation=90)
        plt.show()
        st.pyplot(f)
        st.markdown("##")

        return None

    def get_order_by_time(self):

        orders_per_hour = self.commerce_data.groupby(by=["hour"], as_index=False)[
            "invoice_num"
        ].count()
        orders_per_week = self.commerce_data.groupby(by=["week"], as_index=False)[
            "invoice_num"
        ].count()
        orders_per_month = self.commerce_data.groupby(
            by=["year_month"], as_index=False
        )["invoice_num"].count()
        orders_per_values = {
            "orders_per_hour": orders_per_hour,
            "orders_per_week": orders_per_week,
            "orders_per_month": orders_per_month,
        }

        return orders_per_values

    def vis_contents(self):

        self.insert_columns()
        orders_per_values = self.get_order_by_time()
        st.text("")
        self.bar_plot_single_colour(
            orders_per_values["orders_per_hour"],
            "hour",
            "invoice_num",
            "",
            "No of orders",
            "Number of orders for different hours in a day.",
        )
        st.text("")
        self.bar_plot_single_colour(
            orders_per_values["orders_per_week"],
            "week",
            "invoice_num",
            "",
            "No of orders",
            "Number of orders for different weeks",
        )
        st.text("")
        self.orders_per_month_vis(orders_per_values["orders_per_month"])

        return None


class BasketPriceAnalysis:
    def __init__(self, preprocessed_data):
        self.basket_data = preprocessed_data
        self.basket_data.invoice_date = pd.to_datetime(self.basket_data.invoice_date)

    def basket_price_calculation(self):

        temp_df = self.basket_data.groupby(
            by=["customer_id", "invoice_num"], as_index=False
        )["spend_amount"].sum()
        basket_price = temp_df.rename(columns={"spend_amount": "basket_price"})
        self.basket_data["invoice_date_int"] = self.basket_data["invoice_date"].astype(
            "int64"
        )
        temp_df = self.basket_data.groupby(
            by=["customer_id", "invoice_num"], as_index=False
        )["invoice_date_int"].mean()
        self.basket_data.drop("invoice_date_int", axis=1, inplace=True)
        basket_price.loc[:, "invoice_date"] = pd.to_datetime(
            temp_df["invoice_date_int"]
        )
        basket_price.sort_values("customer_id")[:6]

        return basket_price

    def plot_basket_price(self):

        basket_price = self.basket_price_calculation()
        price_range = [0, 50, 100, 200, 500, 1000, 5000, 50000]
        count_price = []
        for index, price in enumerate(price_range):
            if index == 0:
                continue
            val = basket_price[
                (basket_price["basket_price"] < price)
                & (basket_price["basket_price"] > price_range[index - 1])
            ]["basket_price"].count()
            count_price.append(val)
        f, ax = plt.subplots(figsize=(12, 8))
        colors = ["teal", "salmon", "steelblue", "wheat", "c", "skyblue", "firebrick"]
        labels = [
            "{}<..<{}".format(price_range[i - 1], s)
            for i, s in enumerate(price_range)
            if i != 0
        ]
        sizes = count_price
        explode = [0.0 if sizes[count] < 100 else 0.0 for count in range(len(sizes))]
        ax.pie(
            sizes,
            explode=explode,
            labels=labels,
            colors=colors,
            autopct=lambda percent: "{:1.0f}%".format(percent) if percent > 1 else "",
            shadow=False,
            startangle=0,
        )
        ax.axis("equal")
        ax.set_title("Binning of order amounts", pad=20, fontsize=16)
        st.pyplot(f)

        return None


class CustomerAnalysis:
    def __init__(self, preprocessed_data):
        self.customer_data = preprocessed_data

    def get_ordered_count(self, grouping_element, count_element):

        ordered_value = self.customer_data.groupby(
            by=[grouping_element], as_index=False
        )[count_element].count()

        return ordered_value.sort_values(
            [count_element, grouping_element], ascending=False
        )

    def get_ordered_sum(self, grouping_element, count_element):

        ordered_value = self.customer_data.groupby(
            by=[grouping_element], as_index=False
        )[count_element].sum()

        return ordered_value.sort_values(
            [count_element, grouping_element], ascending=False
        )

    @staticmethod
    def visualize_customers_purchases(values_per_customer):

        f = plt.figure(figsize=(18, 6))
        ax = f.add_subplot(121)
        sns.barplot(
            data=values_per_customer,
            x=values_per_customer["customer_id"],
            y=values_per_customer["invoice_num"],
            palette="Blues_r",
            saturation=0.5,
            order=values_per_customer.sort_values(
                ["invoice_num"], ascending=False
            ).customer_id,
        )
        ax.set_title("Number of orders from different customers", fontsize=16, pad=20)
        plt.xlabel("Customer Id's", fontsize=14)
        plt.ylabel("No of orders", fontsize=14)
        plt.xticks(rotation=90)
        st.pyplot(f)
        st.markdown("##")

        return None

    def vis_contents(self):
        self.visualize_customers_purchases(
            self.get_ordered_count("customer_id", "invoice_num")[0:15]
        )
        self.visualize_customers_purchases(
            self.get_ordered_count("customer_id", "invoice_num")[0:15]
        )


def get_visualizations(data):
     
    country, segment, preprocessed_data = None, None, data
    st.title("Customer Segmentation")
    st.markdown("In-depth visualization of different customers purchases pattern.")
    with st.sidebar:
        analysis = st.selectbox(
            "Select Analysis",
            (
                "Geographic Analysis",
                "Time Analysis",
                "Basket price Analysis",
                "Customer Analysis",
                "RFM Analysis"
            ),
        )

    if analysis == "Geographic Analysis":
        st.subheader("Geographic Analysis")
        st.markdown("##")
        GeographicAnalysis(preprocessed_data).vis_contents()
    elif analysis == "Time Analysis":
        st.subheader("Time based Analysis")
        st.markdown("##")
        TimeAnalysis(preprocessed_data).vis_contents()
    elif analysis == "Basket price Analysis":
        st.subheader("Basket price Analysis")
        st.markdown("##")
        BasketPriceAnalysis(preprocessed_data).plot_basket_price()
    elif analysis == "Customer Analysis":
        st.subheader("Customer Analysis")
        st.markdown("##")
        CustomerAnalysis(preprocessed_data).vis_contents()
    elif analysis == "RFM Analysis":
        country, segment = rfm_data()
        return country, segment
    return None, None
