# Pandas
from pandas import DataFrame

# Visualization
from altair import Chart, condition, layer, selection, value


def interactive_tooltip_chart(
    line_chart: Chart, dataframe: DataFrame, y_column: str = "percentage"
) -> Chart:
    # Make it interactive! Inspired from https://altair-viz.github.io/gallery/multiline_tooltip.html.
    nearest = selection(
        type="single", nearest=True, on="mouseover", fields=["date"], empty="none"
    )
    selectors = (
        Chart(dataframe)
        .mark_point()
        .encode(x="date:T", opacity=value(0),)
        .add_selection(nearest)
    )
    points = line_chart.mark_point().encode(
        opacity=condition(nearest, value(1), value(0))
    )

    # Draw text labels near the points, and highlight based on selection
    text = line_chart.mark_text(align="left", dx=10, dy=-10).encode(
        text=condition(nearest, y_column, value(" "))
    )

    # Draw a rule at the location of the selection
    rules = (
        Chart(dataframe)
        .mark_rule(color="gray")
        .encode(x="date:T",)
        .transform_filter(nearest)
    )

    # Put the five layers into a chart and bind the data
    chart = layer(line_chart, selectors, points, rules, text).properties(
        width=750, height=400
    )
    return chart
