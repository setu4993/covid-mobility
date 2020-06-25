# UI Frameworks
from streamlit import altair_chart, header, markdown, sidebar, subheader, title

from data.load import load_data
from data.partition import partition_data
from data.wrangle import separate_walking_driving
from visualization.visualize import create_chart


def make_webpage():
    title("Exploring Apple's Mobility data for India")

    apple_data = load_data()

    markdown(
        "A few weeks ago, [Apple started publishing](https://www.apple.com/covid19/mobility) mobility data from across the world. The data shows how much people are moving (specifically, making routing requests), comparing to a reference point from January, 2020 before major lockdowns went into place. I have never seen or played with mobility data before, especially from a company like Apple that has customer [privacy](https://www.apple.com/privacy/) at its core and its data so close to its chest, so this was an intriguing opportunity."
    )

    markdown(
        "When I saw this release, I was curious about how movement has changed in India in the last few months."
    )

    header("The Data")

    markdown(
        """
    - Data is baselined with the movement data from January 13, 2020 at 100% for each transportation type.
    - Daily data from countries, regions and cities from across the world. The data from India is available for India as a whole and some of India's major cities (namely Bangalore, Chennai, Delhi, Hyderabad, Mumbai and Pune).
    - Daily means from midnight to midnight PST, not local time. In terms of IST, then, it means the data for January 13, 2020 in the sheet corresponds to approximately (ugh, DST) January 13, 2020 12:30pm to January 14, 2020 12:29pm. In short, everything all dates (and thus the X-axes of all my plots) are off by 1.5 day if I had converted it all to IST. (I did not, because Daylight Savings Time _started_ in mid-March, further complicating the timezone conversions.)
    - Data is available for driving, transit and walking directions, in regions where each of them are available. Since only [driving and walking](https://www.apple.com/ios/feature-availability/) directions are available in India, I can only look at those.
    - Driving directions were not available on Apple Maps in India until fairly recently. Moreover, [90%+ of smartphones in India](https://gs.statcounter.com/os-market-share/mobile/india/) run on Android. Even on iOS, I am highly skeptical of the number of people that use Apple Maps (which this data is from) over Google Maps. So, this could be a very small sample set (which is also why it is only available as an aggregate at the country-level and in some major cities).
    - Data for May 11 and May 12 is not available.
    """
    )

    markdown("With that background, let's dig in...")

    header("Movement across India")

    subheader("Comparing daily driving and walking mobility data for India")
    india_plot_data = partition_data(apple_data)
    india_plot = create_chart(india_plot_data, color_column="transportation_type")
    altair_chart(india_plot)

    markdown(
        "The peaks occur on Saturdays PST, corresponding to Saturday afternoon to Sunday afternoon IST. Leisure travel during weekends is more typical in India. Or maybe those are the times when people actually use maps, whereas commute is not? Either way, the peaks and troughs are interesting."
    )

    markdown(
        "Another thing that was super interesting to me was how the peak keeps increasing and is actually ~40% higher than January 13. Fascinating."
    )

    markdown(
        "As the lockdown starts in March, 2020, I did expect the mobility to sharply go down, which we can see. At the same time, curiously, walking reduces **less** sharply! So, how much did requests for walking directions were reducing compared to driving directions?"
    )

    subheader("Relative number of walking to driving requests across India")
    transportation_type_national_data = separate_walking_driving(india_plot_data)
    transportation_type_national_plot = create_chart(
        transportation_type_national_data, y_column="walking_driving"
    )
    altair_chart(transportation_type_national_plot)

    markdown(
        "The y-axis starts at 0 because I subtracted the baseline from this ratio."
    )

    markdown(
        "Wow, India drives more than walks. Or maybe Indians just don't need walking directions as often as they need driving directions? Hmmm."
    )

    markdown(
        "What's striking, though, is just how much this ratio goes up starting March 23, 2020. There are >50% more walking requests in week 1! This gap slowly reduces over the weeks as the lockdown progresses, though."
    )

    header("Movement in India's cities")

    markdown(
        "We know what's happening on the whole, but does the data tell us any different a story for India's cities?"
    )

    indian_cities_plot_data = partition_data(apple_data, within_region=True)
    indian_cities = indian_cities_plot_data["region"].unique()

    selected_city = sidebar.selectbox(
        "Which city do you want to see the data for?", ["All"] + indian_cities.tolist(),
    )
    if selected_city == "All":
        subheader("Comparing daily driving and walking mobility data for Indian cities")
        indian_cities_plot = create_chart(
            indian_cities_plot_data,
            color_column="region",
            stroke_dash="transportation_type",
        )
        altair_chart(indian_cities_plot)
    else:
        subheader(
            f"Comparing daily driving and walking mobility data for {selected_city}"
        )
        indian_city_plot = create_chart(
            indian_cities_plot_data[indian_cities_plot_data["region"] == selected_city],
            stroke_dash="transportation_type",
        )
        altair_chart(indian_city_plot)

    markdown(
        "Hmmm, Hyderabad clearly has a much higher 'normal' pre-lockdown compared to other Indian cities."
    )

    markdown(
        "Mumbai's lockdown appears to be more severe than other cities because both driving and walking requests fall to <20% (above), and stay there, even when the national requests go well past 30% (above) starting in early May. Moreover, walking direction requests in Mumbai occur only ~30% more frequently (below) than driving in Mumbai."
    )

    markdown(
        "Chennai is starkly different where the relative walking direction requests are up >60% typically and peak at ~160% (below) in the second week of April! I wonder why, but maybe this spike is related to contact tracing following the discovery of a [hotspot](https://www.aljazeera.com/news/2020/04/tablighi-jamaat-event-india-worst-coronavirus-vector-200407052957511.html)?"
    )

    markdown(
        "Delhi's patterns are weird, whereby the walking requests take off sharply with requests peaking to ~100% higher than driving in the first week of the lockdown, but also fall sharply and level off at ~50% over driving thereafter."
    )

    markdown(
        "Bangalore does not seem to be requesting walking directions a lot more than the national average. In fact, that is appears to be just around ~30%."
    )

    markdown(
        "Pune and Hyderabad are both very similar, where walking requests continue at +50% and +40% over driving requests respectively."
    )

    transportation_type_cities_data = separate_walking_driving(indian_cities_plot_data)

    if selected_city == "All":
        subheader("Relative number of walking to driving requests across Indian cities")
        transportation_type_cities_plot = create_chart(
            transportation_type_cities_data,
            y_column="walking_driving",
            color_column="region",
        )
        altair_chart(transportation_type_cities_plot)
    else:
        subheader(f"Relative number of walking to driving requests in {selected_city}")
        transportation_type_cities_plot = create_chart(
            transportation_type_cities_data[
                transportation_type_cities_data["region"] == selected_city
            ],
            y_column="walking_driving",
            color_column="region",
        )
        altair_chart(transportation_type_cities_plot)

    subheader("Update (June 13, 2020)")

    markdown(
        "I just added interactive tooltips to all of the visualizations above that show the value of the Y-axis for the date hovered on. Try it!"
    )

    markdown(
        "Additionally, I moved the filter to the sidebar, and updated the data to be updated to June 11, 2020, latest avaialble as I write this. As the lockdown begins to open up, I think these trends could become less interesting and return back to 'normal'. Or maybe people will voluntarily still continue to be on lockdown. We'll see..."
    )

    markdown(
        """
        A few additional notes on what I just saw from the graphs above:
        - Walking (relative to driving) continues to go down as the lockdown progresses and the country starts to open up. This is slightly depressing.
        - Mumbai continues to have very limited mobility, but driving dominates walking.
        - Hyderabad appears to be moving towards pre-lockdown levels of mobility for driving and walking is reducing in relation.
        - Most cities are back at or below the baseline walking to driving ratio, with Pune being the only exception.
        - Pune is interesting; mobility is surely going up for both walking and driving, but at more or less the same rate, and thus maybe people continue to prefer walking to driving?
        """
    )

    header("About")

    markdown(
        "Built and maintained by [Setu Shah](https://setu.me). Some more details about it on my [micro-blog](https://micro.setu.me/posts/playing-apple-covid-mobility-india/)."
    )

    markdown(
        "© 2020 [Setu Shah](https://setu.me). All rights reserved. | All of my source code is on [GitHub](https://github.com/setu4993/covid-mobility) and the data is from [Apple](https://www.apple.com/covid19/mobility)."
    )


if __name__ == "__main__":
    make_webpage()
