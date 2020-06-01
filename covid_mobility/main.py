# Frameworks
import streamlit as st

from data.load import load_data
from data.partition import partition_data
from data.wrangle import separate_walking_driving
from visualization.visualize import altair_chart

if __name__ == "__main__":
    st.title("Exploring Apple's Mobility data for India")

    apple_data = load_data()

    india_plot_data = partition_data(apple_data)
    india_plot = altair_chart(india_plot_data)
    st.altair_chart(india_plot)

    indian_cities_plot_data = partition_data(apple_data, within_region=True)

    indian_cities_plot = altair_chart(
        indian_cities_plot_data,
        color_column="region",
        stroke_dash="transportation_type",
    )

    st.altair_chart(indian_cities_plot)

    city = st.selectbox(
        "Which city do you want to see the data for?",
        ("All", "Bangalore", "Chennai", "Delhi", "Hyderabad", "Mumbai", "Pune"),
    )

    if city == "All":
        st.altair_chart(indian_cities_plot)
    else:
        indian_city_plot = altair_chart(
            indian_cities_plot_data[indian_cities_plot_data["region"] == city],
            stroke_dash="transportation_type",
        )
        st.altair_chart(indian_city_plot)

    transportation_type_cities_data = separate_walking_driving(indian_cities_plot_data)

    transportation_type_cities_plot = altair_chart(
        transportation_type_cities_data,
        y_column="walking_driving",
        color_column="region",
    )
    st.altair_chart(transportation_type_cities_plot)

    if city == "All":
        st.altair_chart(transportation_type_cities_plot)
    else:
        transportation_type_cities_plot = altair_chart(
            transportation_type_cities_data[
                transportation_type_cities_data["region"] == city
            ],
            y_column="walking_driving",
            color_column="region",
        )
        st.altair_chart(transportation_type_cities_plot)
