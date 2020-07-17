"""Exploring US Bikeshare Data Project by Joseph (Josh) White"""

import time
import tkinter as tk
import pandas as pd

CITY_DATA = {
    "chicago": "chicago.csv",
    "new york city": "new_york_city.csv",
    "washington": "washington.csv",
}

DAY_OPTIONS = [
    "All",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]

MONTH_OPTIONS = ["All", "January", "February", "March", "April", "May", "June"]


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


def radio_buttons_from_list(parent, items, variable, command):
    """Instantiate radio buttons from a list of items."""

    for row, item in enumerate(items):
        tk.Radiobutton(
            parent,
            text=item.title(),
            variable=variable,
            value=item,
            anchor="w",
            justify="left",
            command=command,
        ).grid(row=row, column=0, sticky="we")


def stat_display_labels(parent, text, labels, row=0, column=0, columnspan=1):
    """Instantiate static parts of statistics frames."""

    frame = tk.LabelFrame(parent, text=text, padx=5, pady=5)
    frame.grid(
        row=row, column=column, padx=5, pady=5, sticky="w", columnspan=columnspan
    )
    stats_label = tk.Label(frame, text="\n".join(labels), justify="right")
    stats_label.grid(row=0, column=0)
    return frame


class Application(tk.Frame):
    """Main entrypoint for the statistics display application instantiated in main function"""

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_selections_column()
        self.create_controls()

        self.stats_frame = tk.Frame(self)
        self.stats_frame.grid(row=0, column=2, rowspan=3, sticky="ns")

        self.display_time_stats()
        self.display_station_stats()
        self.display_trip_stats()
        self.display_user_stats()

        self.status = tk.Label(self, bd=1, relief="sunken", anchor="sw")
        self.status.grid(row=5, column=0, columnspan=3, sticky="we")
        self.update_stats()

        self.raw_data_index = 0

    def create_selections_column(self):
        """Provides radio buttons for the user to select filters"""

        self.selections = dict(
            city=tk.StringVar(None, "chicago"),
            day=tk.StringVar(None, "All"),
            month=tk.StringVar(None, "All"),
        )

        self.city_frame = tk.LabelFrame(self, text="City", padx=5, pady=5)
        self.city_frame.grid(row=0, column=0, padx=5, pady=5, sticky="we")
        radio_buttons_from_list(
            self.city_frame,
            CITY_DATA.keys(),
            self.selections["city"],
            self.prompt_load_data,
        )

        self.day_frame = tk.LabelFrame(self, text="Week Day", padx=5, pady=5)
        self.day_frame.grid(row=1, column=0, padx=5, pady=5, sticky="we")
        radio_buttons_from_list(
            self.day_frame, DAY_OPTIONS, self.selections["day"], self.prompt_load_data
        )

        self.month_frame = tk.LabelFrame(self, text="Month", padx=5, pady=5)
        self.month_frame.grid(row=2, column=0, padx=5, pady=5, sticky="we")
        radio_buttons_from_list(
            self.month_frame,
            MONTH_OPTIONS,
            self.selections["month"],
            self.prompt_load_data,
        )

    def create_controls(self):
        """Create the Load Data and Quit Buttons"""

        self.button_frame = tk.LabelFrame(self, text="Controls", padx=5, pady=5)
        self.button_frame.grid(row=0, column=1, padx=5, pady=5, sticky="n")
        self.load_data = tk.Button(
            self.button_frame, text="Load Data", command=self.update_stats
        )
        self.load_data.grid(row=0)

        self.print_data = tk.Button(
            self.button_frame, text="Print Data", command=self.print_raw_data,
        )
        self.print_data.grid(row=1)

        self.quit = tk.Button(
            self.button_frame, text="Quit", fg="red", command=self.master.destroy
        )
        self.quit.grid(row=2)

    def display_time_stats(self):
        """Creates frame and labels for time stats"""

        self.time_frame = stat_display_labels(
            self.stats_frame,
            "Time Stats",
            [
                "The busiest month was:",
                "The busiest day of the week was:",
                "The busiest start hour was:",
            ],
            row=0,
            columnspan=2,
        )
        self.time_stats_data = tk.Label(self.time_frame, justify="left")
        self.time_stats_data.grid(row=0, column=2)

    def display_station_stats(self):
        """Creates frame and labels for station stats"""

        self.station_frame = stat_display_labels(
            self.stats_frame,
            "Station Stats",
            [
                "The most popular start station was:",
                "The most popular end station was:",
                "The most popular start/end station combination was:",
            ],
            row=1,
            columnspan=5,
        )
        self.station_stats_data = tk.Label(self.station_frame, justify="left")
        self.station_stats_data.grid(row=0, column=1)

    def display_trip_stats(self):
        """Creates frame and labels for trip stats"""

        self.trip_frame = stat_display_labels(
            self.stats_frame,
            "Trip Stats",
            ["The total travel time was:", "The mean travel time was:"],
            row=0,
            column=2,
        )
        self.trip_stats_data = tk.Label(self.trip_frame, justify="left")
        self.trip_stats_data.grid(row=0, column=1)

    def display_user_stats(self):
        """Creates frame and labels for user stats"""

        self.user_frame = tk.LabelFrame(
            self.stats_frame, text="User Types", padx=5, pady=5
        )
        self.user_frame.grid(row=3, padx=5, pady=5, sticky="w")
        self.user_stats_data = tk.Label(self.user_frame, justify="left")
        self.user_stats_data.pack()

        self.gender_frame = tk.LabelFrame(
            self.stats_frame, text="User Gender", padx=5, pady=5
        )
        self.gender_frame.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        self.gender_stats_data = tk.Label(self.gender_frame, justify="left")
        self.gender_stats_data.pack()

        self.age_frame = stat_display_labels(
            self.stats_frame,
            "Age Stats",
            [
                "Oldest Rider Birth Year:",
                "Youngest Rider Birth Year:",
                "Most common birth year:",
            ],
            row=4,
            columnspan=2,
        )
        self.age_stats_data = tk.Label(self.age_frame, justify="left")
        self.age_stats_data.grid(row=0, column=1)

    def update_stats(self):
        """Provides the logic for updating all statistics in right column"""

        self.raw_data_index = 0
        start_time = time.time()
        data_frame = load_data(self.selections)
        user_stats = get_user_stats(data_frame)

        self.time_stats_data.config(text=get_time_stats(data_frame))
        self.station_stats_data.config(text=get_station_stats(data_frame))
        self.trip_stats_data.config(text=get_trip_duration_stats(data_frame))

        self.user_stats_data.config(text=user_stats[0])
        self.gender_stats_data.config(text=user_stats[1])
        self.age_stats_data.config(text=user_stats[2])
        self.status.config(
            text=f"Updated statistics in {round((time.time() - start_time), 2)} seconds. Modify filters using left radio buttons as desired..."
        )

    def print_raw_data(self):
        """Print a slice of date_frame in the terminal window."""

        start_time = time.time()
        data_frame = load_data(self.selections)
        if self.raw_data_index < len(data_frame) - 1:
            if self.raw_data_index + 5 < len(data_frame) - 1:
                print(data_frame[self.raw_data_index : self.raw_data_index + 5])
            else:
                print(data_frame[self.raw_data_index :])
        else:
            print("All raw data for this data frame has been printed")
        self.raw_data_index += 5
        self.status.config(
            text=f"Next 5 lines of raw data printed in terminal.This took {round((time.time() - start_time), 2)} seconds."
        )

    def prompt_load_data(self):
        """Prompt user to click Load Data button if selections updated."""

        self.status.config(
            text="Selections modified! Click Load Data to update statistics when ready..."
        )


def main():
    """Launch the stats window"""

    root = tk.Tk()
    root.title("Exploring US Bikeshare Data")
    app = Application(master=root)
    print("Application loaded! Please use the GUI window to continue...")
    app.mainloop()


if __name__ == "__main__":
    main()
