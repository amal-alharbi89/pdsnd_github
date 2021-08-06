
import datetime
import time
import pandas as pd
import numpy as np


CITY_DATA = {'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv'}
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington).
    city = input("Please enter Which city from (Chicago, New York, Washington) you would like to analyze: ").lower()
    while city not in CITY_DATA:
        city = input("Sorry we can not identify the city,Please enter one city from the following (Chicago, New York, Washington) to analyze: ").lower()

    #  get user input for month (all, january, february, ... , june)
    month = input("name a month ('January', 'February', 'March', 'April', 'May', 'June') to filter by  , or \"all\" to apply no month filter: ").lower()
    while month not in ('all','january', 'february', 'march', 'april', 'may', 'june'):
        month = input("Sorry we can not identify your input, Please name a month ('January', 'February', 'March', 'April', 'May', 'June') to filter by, or \"all\" to apply no month filter: ").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("name a day ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday') to filter by, or \"all\" to apply no day filter: ").lower()
    while day not in ('all','sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'):
        day = input("Sorry we can not identify your input, Please name of a day ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday') to filter by, or \"all\" to apply no day filter: ").lower()

    print('-'*40)
    return city, month, day

# This code has been taken from udacity Practice Solution #3 (https://classroom.udacity.com/nanodegrees/nd104-connect/parts/1511355b-2497-4361-9d6a-b6d67355c98e/modules/a9663bb9-9a53-4ead-8d38-06562e38fee6/lessons/ee7d089a-4a92-4e5d-96d2-bb256fae28e9/concepts/d82f015d-fe75-4de1-b76b-0fdebe4cd9d7)
def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int

        month = MONTHS.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # if condition in case the user select specific month or day, there is no need to repeat the same month or day
    if month == 'all':
        # display the most common month
        common_month = df['month'].mode()[0]
        # display the count for most common month
        common_month_count = df['month'].value_counts().max()
        print("For {} city, The most popular month of traveling is: {} / count: {}".format(city, MONTHS[common_month - 1].title(), common_month_count))

    if day == 'all':
        # display the most common day of week
        common_day = df['day_of_week'].mode()[0]
        # display the count for most common day
        common_day_count = df['day_of_week'].value_counts().max()
        print("For {} city, The most popular day for traveling is: {} / count: {} ".format(city, common_day, common_day_count))

    # display the most common start hour
    # extract hours from Start Time to create new columns
    df['hour'] = df['Start Time'].dt.hour
    common_start_hour = df['hour'].mode()[0]
    # display the count for most common hour
    common_hour_count = df['hour'].value_counts().max()
    print("For {} city, The most peak hour of traveling is: {} / count: {}".format(city, common_start_hour, common_hour_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    # display count for most common used start station
    count_start_station = df['Start Station'].value_counts().max()
    print("For {} city, The most common start station is: {} / count:{}".format(city,common_start_station, count_start_station))

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    # display count for most common used end station
    count_end_station = df['End Station'].value_counts().max()
    print("For {} city, The most common end station is: {} / count:{}".format(city, common_end_station, count_end_station))


    # create Start to End Station coulmns to display most frequent combination of start station and end station trip
    frequent_journey = (df['Start Station'] + ' TO ' + df['End Station']).mode()[0]
    # display count for most common trip
    journey_count = (df['Start Station'] + ' TO ' + df['End Station']).value_counts().max()
    print("For {} city, The most frequent journey is from: {} / count:{}".format(city, frequent_journey, journey_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()

    # convert total travel time seconds to days,hours,minutes which will be more efficient and easy to read
    total_travel_hours = datetime.timedelta(seconds=int(total_travel_time))

    # display the total travel time count
    total_travel_count = df['Trip Duration'].count()
    print("For {} city, The total hours of traveling is: {} (The total in Seconds is: {}) / count: {}".format(city, total_travel_hours,total_travel_time, total_travel_count))

    # display travel time mean
    travel_time_average =df['Trip Duration'].mean()
    #convert travel time mean seconds to days,hours,minutes
    travel_average_hours = datetime.timedelta(seconds=int(travel_time_average))
    print("For {} city, The average hours of traveling is: {} (The average in Seconds is: {})".format(city,travel_average_hours, travel_time_average))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df['User Type'].value_counts()
    print("For {} city, the user types are: \n{}".format(city, user_type))

    # since the gender and birth year columns are not in washington.csv , use if to check the city is not washington
    if city != 'washington':
        # Display counts of gender
        gender_count = df['Gender'].value_counts()
        print("For {} city, the gender count is: \n{}".format(city, gender_count))

        # Display earliest, most recent, and most common year of birth
        earliest_birth_year = df['Birth Year'].min()
        print("For {} city, the earliest year of birth is: {}".format(city, earliest_birth_year))
        recent_birth_year = df['Birth Year'].max()
        print("For {} city, the most recent year of birth is: {}".format(city, recent_birth_year))
        common_birth_year = df['Birth Year'].mode()[0]
        print("For {} city, the most common year of birth is: {}".format(city, common_birth_year))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(city):

    """
        Displays raw data upon user request

        Args:
            (str) city - name of the city to load data file into a dataframe and show the raw data

        """
    user_response = input("Would like to explore the first 5 rows of US bikeshare data? ")
    rows_number = 0
    # load the raw data without any modification like (month,day od week, hour) coulmns we added in df dataframe so the user can see the raw data
    raw_data = pd.read_csv(CITY_DATA[city])
    # while loop to continue prompts and displays the rows until the user says 'no'

    while user_response.lower() == 'yes':
        # added 4 because the rows starts from zero
        print("The first 5 rows: \n {}".format(raw_data.loc[rows_number:rows_number+4]))
        user_response = input("Would like to explore the next 5 rows of US bikeshare data? ")
        rows_number += 5


def main():
    while True:
        # make city, month, day global so we can use them throughout the program
        global city, month, day
        city, month, day = get_filters()
        df = load_data(city, month, day)

        # call functions
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
