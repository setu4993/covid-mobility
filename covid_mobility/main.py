# Frameworks
import streamlit as st

from data.load import load_data
from data.partition import partition_data
from data.wrangle import separate_walking_driving
from visualization.visualize import altair_chart


def make_webpage():
    st.title("Exploring Apple's Mobility data for India")

    apple_data = load_data()

    st.markdown(
        "A few weeks ago, [Apple started publishing](https://www.apple.com/covid19/mobility) mobility data from across the world. The data shows how much people are moving (specifically, making routing requests), comparing to a reference point from January, 2020 before major lockdowns went into place. I have never seen or played with mobility data before, especially from a company like Apple that has customer [privacy](https://www.apple.com/privacy/) at its core and its data so close to its chest, so this was an intriguing opportunity."
    )

    st.markdown(
        "When I saw this release, I was curious about how movement has changed in India in the last few months."
    )

    st.header("The Data")

    st.markdown(
        """
    - Data is baselined with the movement data from January 13, 2020 at 100% for each transportation type.
    - Daily data from countries, regions and cities from across the world. The data from India is available for India as a whole and some of India's major cities (namely Bangalore, Chennai, Delhi, Hyderabad, Mumbai and Pune).
    - Daily means from midnight to midnight PST, not local time. In terms of IST, then, it means the data for January 13, 2020 in the sheet corresponds to approximately (ugh, DST) January 13, 2020 12:30pm to January 14, 2020 12:29pm. In short, everything all dates (and thus the X-axes of all my plots) are off by 1.5 day if I had converted it all to IST. (I did not, because Daylight Savings Time _started_ in mid-March, further complicating the timezone conversions.)
    - Data is available for driving, transit and walking directions, in regions where each of them are available. Since only [driving and walking](https://www.apple.com/ios/feature-availability/) directions are available in India, I can only look at those.
    - Driving directions were not available on Apple Maps in India until fairly recently. Moreover, [90%+ of smartphones in India](https://gs.statcounter.com/os-market-share/mobile/india/) run on Android. Even on iOS, I am highly skeptical of the number of people that use Apple Maps (which this data is from) over Google Maps. So, this could be a very small sample set (which is also why it is only available as an aggregate at the country-level and in some major cities).
    - Data for May 11 and May 12 is not available.
    """
    )

    st.write("With that background, let's dig in...")

    st.header("Movement across India")

    st.subheader("Comparing daily driving and walking mobility data for India")
    india_plot_data = partition_data(apple_data)
    india_plot = altair_chart(india_plot_data, color_column="transportation_type")
    st.altair_chart(india_plot)

    st.markdown(
        "The peaks occur on Saturdays PST, corresponding to Saturday afternoon to Sunday afternoon IST. Leisure travel during weekends is more typical in India. Or maybe those are the times when people actually use maps, whereas commute is not? Either way, the peaks and troughs are interesting."
    )

    st.markdown(
        "Another thing that was super interesting to me was how the peak keeps increasing and is actually ~40% higher than January 13. Fascinating."
    )

    st.markdown(
        "As the lockdown starts in March, 2020, I did expect the mobility to sharply go down, which we can see. At the same time, curiously, walking reduces **less** sharply! So, how much did requests for walking directions were reducing compared to driving directions?"
    )

    st.subheader("Relative number of walking to driving requests across India")
    transportation_type_national_data = separate_walking_driving(india_plot_data)
    transportation_type_national_plot = altair_chart(
        transportation_type_national_data, y_column="walking_driving"
    )
    st.altair_chart(transportation_type_national_plot)

    st.markdown(
        "The y-axis starts at 0 because I subtracted the baseline from this ratio."
    )

    st.markdown(
        "Wow, India drives more than walks. Or maybe Indians just don't need walking directions as often as they need driving directions? Hmmm."
    )

    st.markdown(
        "What's striking, though, is just how much this ratio goes up starting March 23, 2020. There are >50% more walking requests in week 1! This gap slowly reduces over the weeks as the lockdown progresses, though."
    )

    st.header("Movement in India's cities")

    st.markdown(
        "We know what's happening on the whole, but does the data tell us any different a story for India's cities?"
    )

    indian_cities_plot_data = partition_data(apple_data, within_region=True)
    indian_cities = indian_cities_plot_data["region"].unique()

    selected_city = st.selectbox(
        "Which city do you want to see the data for?", ["All"] + indian_cities.tolist(),
    )
    if selected_city == "All":
        st.subheader(
            "Comparing daily driving and walking mobility data for Indian cities"
        )
        indian_cities_plot = altair_chart(
            indian_cities_plot_data,
            color_column="region",
            stroke_dash="transportation_type",
        )
        st.altair_chart(indian_cities_plot)
    else:
        st.subheader(
            f"Comparing daily driving and walking mobility data for {selected_city}"
        )
        indian_city_plot = altair_chart(
            indian_cities_plot_data[indian_cities_plot_data["region"] == selected_city],
            stroke_dash="transportation_type",
        )
        st.altair_chart(indian_city_plot)

    st.markdown(
        "Hmmm, Hyderabad clearly has a much higher 'normal' pre-lockdown compared to other Indian cities."
    )

    st.markdown(
        "Mumbai's lockdown appears to be more severe than other cities because both driving and walking requests fall to <20% (above), and stay there, even when the national requests go well past 30% (above) starting in early May. Moreover, walking direction requests in Mumbai occur only ~30% more frequently (below) than driving in Mumbai."
    )

    st.markdown(
        "Chennai is starkly different where the relative walking direction requests are up >60% typically and peak at ~160% (below) in the second week of April! I wonder why, but maybe this spike is related to contact tracing following the discovery of a [hotspot](https://www.aljazeera.com/news/2020/04/tablighi-jamaat-event-india-worst-coronavirus-vector-200407052957511.html)?"
    )

    st.markdown(
        "Delhi's patterns are weird, wherein the walking take off sharply with requests ~100% higher than driving in the first week of the lockdown, but fall sharply and level off at ~50% over driving thereafter."
    )

    st.markdown(
        "Bangalore does not seem to be requesting walking directions a lot more than the national average. In fact, that is appears to be just around ~30%."
    )

    st.markdown(
        "Pune and Hyderabad are both very similar, where walking requests continue at +50% and +40% over driving requests respectively."
    )

    transportation_type_cities_data = separate_walking_driving(indian_cities_plot_data)

    if selected_city == "All":
        st.subheader(
            "Relative number of walking to driving requests across Indian cities"
        )
        transportation_type_cities_plot = altair_chart(
            transportation_type_cities_data,
            y_column="walking_driving",
            color_column="region",
        )
        st.altair_chart(transportation_type_cities_plot)
    else:
        st.subheader(
            f"Relative number of walking to driving requests in {selected_city}"
        )
        transportation_type_cities_plot = altair_chart(
            transportation_type_cities_data[
                transportation_type_cities_data["region"] == selected_city
            ],
            y_column="walking_driving",
            color_column="region",
        )
        st.altair_chart(transportation_type_cities_plot)


if __name__ == "__main__":
    make_webpage()
