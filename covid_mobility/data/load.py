# Standard libraries
from os.path import exists, isfile

# Pandas
from pandas import DataFrame, read_csv

# UI Frameworks
from streamlit import cache


@cache
def load_data(
    data_file: str = "./data/applemobilitytrends-2020-06-11.csv",
) -> DataFrame:
    assert exists(data_file) and isfile(data_file)
    # Read Apple mobility data from CSV.
    apple_data = read_csv(data_file)

    # Fill NaNs with empty strings for all name columns.
    apple_data["alternative_name"].fillna("", inplace=True)
    apple_data["sub-region"].fillna("", inplace=True)
    apple_data["country"].fillna("", inplace=True)
    return apple_data
