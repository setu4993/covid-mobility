from os.path import exists, isfile

import pandas as pd

import altair as alt

import streamlit as st


def load_data(data_file: str = "./data/applemobilitytrends-2020-05-24.csv") -> pd.DataFrame:
    assert exists(data_file) and isfile(data_file)
    # Read Apple mobility data from CSV.
    apple_data = pd.read_csv(data_file)

    # Fill NaNs with empty strings for all name columns.
    apple_data["alternative_name"].fillna("", inplace=True)
    apple_data["sub-region"].fillna("", inplace=True)
    apple_data["country"].fillna("", inplace=True)
    return apple_data


def india_chart_plot_data(mobility_data: pd.DataFrame) -> pd.DataFrame:
    india_data = apple_data[apple_data["region"] == "India"]
    columns_for_plots = [col for col in india_data.columns if col.startswith("2020")]
    columns_for_plots.append("transportation_type")
    return india_data[columns_for_plots].melt(id_vars="transportation_type", value_name="percentage", var_name="date")


def indian_cities_chart_plot_data(mobility_data: pd.DataFrame) -> pd.DataFrame:
    india_cities_data = apple_data[apple_data["country"].str.contains("India")]
    columns_for_plots = [col for col in india_cities_data.columns if col.startswith("2020")]
    columns_for_plots.extend(["transportation_type", "region"])
    return india_cities_data[columns_for_plots].melt(id_vars=["transportation_type", "region"], value_name="percentage", var_name="date")


if __name__ == "__main__":
    st.title("Exploring Apple's Mobility data for India")

    apple_data = load_data()


    india_plot_data = india_chart_plot_data(apple_data)
    india_plot = alt.Chart(india_plot_data, width=750, height=400).mark_line().encode(x="date:T", y="percentage", color="transportation_type")
    st.altair_chart(india_plot)

    indian_cities_plot_data = indian_cities_chart_plot_data(apple_data)


    indian_cities_plot = alt.Chart(indian_cities_plot_data, width=750, height=400).mark_line().encode(x="date:T", y="percentage", color="region", strokeDash="transportation_type")
    st.altair_chart(indian_cities_plot)

    city = st.selectbox(
    "How would you like to be contacted?",
    ("Bangalore", "Mumbai", "Delhi")
    )
    indian_cities_plot = alt.Chart(indian_cities_plot_data[indian_cities_plot_data["region"] == city], width=750, height=400).mark_line().encode(x="date:T", y="percentage", color="region", strokeDash="transportation_type")
    st.altair_chart(indian_cities_plot)


