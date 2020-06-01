# Visualization
import altair as alt


def altair_chart(
    dataframe,
    y_column: str = "percentage",
    color_column: str = None,
    stroke_dash: str = None,
) -> alt.Chart:
    chart = (
        alt.Chart(dataframe, width=750, height=400)
        .mark_line()
        .encode(x="date:T", y=y_column)
    )
    if color_column is not None:
        chart = chart.encode(color=color_column)
    if stroke_dash is not None:
        chart = chart.encode(strokeDash=stroke_dash)
    return chart
