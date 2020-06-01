from os.path import exists, isfile
import pandas as pd
import streamlit as st

@st.cache
def load_data(data_file: str = "./data/applemobilitytrends-2020-05-24.csv") -> pd.DataFrame:
    assert exists(data_file) and isfile(data_file)
    # Read Apple mobility data from CSV.
    apple_data = pd.read_csv(data_file)

    # Fill NaNs with empty strings for all name columns.
    apple_data["alternative_name"].fillna("", inplace=True)
    apple_data["sub-region"].fillna("", inplace=True)
    apple_data["country"].fillna("", inplace=True)
    return apple_data
