import pandas as pd

CITY_DATA = {
    "chicago": "chicago.csv",
    "new york city": "new_york_city.csv",
    "washington": "washington.csv",
}


def load_data(selections):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        data_frame - Pandas DataFrame containing city data filtered by month and day
    """
    city = selections["city"].get()
    month = selections["month"].get()
    day = selections["day"].get()
    data_frame = pd.read_csv(CITY_DATA[city])

    data_frame["Start Time"] = pd.to_datetime(data_frame["Start Time"])

    data_frame["month"] = data_frame["Start Time"].dt.month_name()
    data_frame["day_of_week"] = data_frame["Start Time"].dt.day_name()

    if month != "All":
        data_frame = data_frame[data_frame["month"] == month]

    if day != "All":
        data_frame = data_frame[data_frame["day_of_week"] == day]

    return data_frame


def get_time_stats(data_frame):
    """Displays statistics on the most frequent times of travel."""

    popular_time = data_frame["Start Time"].dt.hour.mode()[0]
    if popular_time < 12:
        popular_time = f"{popular_time} AM"
    elif popular_time == 0:
        popular_time = "12 AM"
    elif popular_time == 12:
        popular_time = "12 PM"
    else:
        popular_time = f"{popular_time % 12} PM"

    return "\n".join(
        [
            format(data_frame["month"].mode()[0]),
            format(data_frame["day_of_week"].mode()[0]),
            popular_time,
        ]
    )


def get_station_stats(data_frame):
    """Displays statistics on the most popular stations and trip."""

    return "\n".join(
        [
            format(data_frame["Start Station"].mode()[0]),
            format(data_frame["End Station"].mode()[0]),
            format(
                data_frame["Start Station"]
                .str.cat(data_frame["End Station"], sep=" to ")
                .mode()[0]
            ),
        ]
    )


def get_trip_duration_stats(data_frame):
    """Displays statistics on the total and average trip duration."""

    return "\n".join(
        [
            "{} years".format(
                round(data_frame["Trip Duration"].sum() / (3600 * 24 * 365.33), 2)
            ),
            "{} minutes".format(round(data_frame["Trip Duration"].mean() / 60, 2)),
        ]
    )


def trim_pd_series(series):
    """Helper function to remove extra info from Pandas Series printing"""

    return "\n".join(str(series).split("\n")[:-1])


def get_user_stats(data_frame):
    """Displays statistics on bikeshare users."""

    results = []

    results.append(trim_pd_series(data_frame["User Type"].value_counts()))

    try:
        results.append(trim_pd_series(data_frame["Gender"].value_counts()))
    except KeyError:
        results.append("Gender Data\nNot Available")

    try:
        results.append(
            "\n".join(
                [
                    str(int(data_frame["Birth Year"].min())),
                    str(int(data_frame["Birth Year"].max())),
                    str(int(data_frame["Birth Year"].mode()[0])),
                ]
            )
        )
    except KeyError:
        results.append("Age Data\nNot Available")
    return results
