# Pandas
import pandas as pd


def separate_walking_driving(source: pd.DataFrame) -> pd.DataFrame:
    walking = (
        source[source["transportation_type"] == "walking"]
        .rename(columns={"percentage": "walking"})
        .drop(columns=["transportation_type"])
    )
    driving = (
        source[source["transportation_type"] == "driving"]
        .rename(columns={"percentage": "driving"})
        .drop(columns=["transportation_type"])
    )
    combined = walking.merge(driving)
    combined["walking_driving"] = combined["walking"] / combined["driving"]
    combined["walking_driving"] -= 1.0
    return combined
