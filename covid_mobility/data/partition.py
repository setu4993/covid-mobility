# Pandas
import pandas as pd


def partition_data(
    mobility_data: pd.DataFrame, within_region: bool = False
) -> pd.DataFrame:
    partitioned_data = (
        mobility_data[mobility_data["country"].str.contains("India")]
        if within_region
        else mobility_data[mobility_data["region"] == "India"]
    )

    data_columns = [col for col in partitioned_data.columns if col.startswith("2020")]
    id_columns = ["transportation_type"]

    if within_region:
        id_columns.append("region")
    melted_data = partitioned_data[data_columns + id_columns].melt(
        id_vars=id_columns, value_name="percentage", var_name="date"
    )
    return melted_data
