import time
#import datetime as dt
import pandas as pd
import numpy as np

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')
    # get the input from the user for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('\nWhich city would you like to filter by? New York City, Chicago or Washington?\n').title()
        if city not in  ('New York City' , 'Chicago' , 'Washington'):
            print('\nWrong Entrance, please Try again!\n')
        else:
            break

    # get user input for month (all the months, january, february, ... , june)
    while True:
        month = input('\nWhich city would you like to filter by? January, February, March, April, May, June or type "all" if you do not to filter by a specific month?\n').title()
        if month not in ('January', 'February', 'March', 'April', 'May', 'June','All'):
            print('\nWrong Entrance, please Try again!\n')
        else:
            break

    # get user input for day of week (all the days, monday, tuesday,... sunday)
    while True:
        day = input('\nWhich day of week would you like to filter by? Saturday, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday or type "all" if you do not to filter by a specific day?\n').title()
        if day not in ('Saturday','Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'All'):
            print('\nWrong Entrance, please Try again!\n')
        else:
            break


    print('-'*40)
    return city, month, day


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
    df = pd.read_csv(CITY_DATA.get(city))

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of the week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.strftime("%A")
    #df['day_of_week'] = df['Start Time'].dt.weekday_name


    # filter by month if applicable
    if month != 'All':
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) +1 #7ta brob3

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print('The most common month:', common_month)


    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('The most common day of week:', common_day)


    # display the most common start hour
    common_hr = df['Start Time'].dt.hour.mode()[0]
    print('The most common start hour:', common_hr)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_Start_Station = df['Start Station'].value_counts().idxmax()
    print('The most commonly used start station:', common_Start_Station)

    # display most commonly used end station
    common_End_Station = df['End Station'].value_counts().idxmax()
    print('The most commonly used end station:', common_End_Station)

    # display most frequent combination of start station and end station trip
    # combination = df.groupby(['Start Station', 'End Station']).count()
    print('\nmost frequent combination of start station and end station trip:', common_Start_Station, " To ", common_End_Station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = sum(df['Trip Duration'])
    print('The total travel time:', total_travel_time/(60*60*24), " Days")

    # display mean travel time
    av_trip_duration =  df['Trip Duration'].mean()
    print('The average trip duration: ',av_trip_duration , " Seconds")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('User Types:\n', user_types)

    # Display counts of gender
    try:
      gender_types = df['Gender'].value_counts()
      print('\nGender Types:\n', gender_types)
    except KeyError:
      print("\nGender Types: Sorry, No data for this month")

    # Display earliest, most recent, and most common year of birth
    try:
      earliest = df['Birth Year'].min()
      print('\nEarliest Year:', earliest)
    except KeyError:
      print("\nEarliest Year: Sorry, No data for this month")

    try:
      most_recent = df['Birth Year'].max()
      print('\nMost Recent Year:', most_recent)
    except KeyError:
      print("\nMost Recent Year: Sorry, No data for this month")

    try:
      most_common = df['Birth Year'].value_counts().idxmax()
      print('\nMost Common Year:', most_common)
    except KeyError:
      print("\nMost Common Year: Sorry, No data for this month")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """
    Asks user if they want to see 5 lines of raw data.
    Returns the 5 lines of raw data if user inputs `yes`. Iterate until user response with a `no`

    """

    data = 0

    while True:
        answer = input('\nWould you like to see 5 lines of raw data? Enter yes or no: ')
        if answer.lower() == 'yes':
            print (df[data:data+5])
            data += 5

        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no:\n')
        if restart.lower() != 'yes':
            print('\n\nThank you :)')
            break



if __name__ == "__main__":
    main()
