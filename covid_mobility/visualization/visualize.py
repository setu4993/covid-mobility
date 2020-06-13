# Pandas
from pandas import DataFrame

# Visualization
from altair import Chart

# Local
from .interactive import interactive_tooltip_chart


def altair_chart(
    dataframe: DataFrame,
    y_column: str = "percentage",
    color_column: str = None,
    stroke_dash: str = None,
    interactive: bool = True,
) -> Chart:
    line_chart = (
        Chart(dataframe, width=750, height=400)
        .mark_line()
        .encode(x="date:T", y=y_column)
    )
    if color_column is not None:
        line_chart = line_chart.encode(color=color_column)
    if stroke_dash is not None:
        line_chart = line_chart.encode(strokeDash=stroke_dash)

    if interactive:
        return interactive_tooltip_chart(line_chart, dataframe, y_column)
    else:
        return line_chart
