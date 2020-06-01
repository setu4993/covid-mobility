import altair as alt


def altair_chart(dataframe, color_column: str="transportation_type", stroke_dash: str=None) -> alt.Chart:
    chart = alt.Chart(dataframe, width=750, height=400).mark_line().encode(x="date:T", y="percentage", color=color_column, tooltip=['transportation_type'])
    if stroke_dash is not None:
        chart = chart.encode(strokeDash=stroke_dash)
    return chart
