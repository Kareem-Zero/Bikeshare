import time
import pandas as pd
import numpy as np

CITY_DATA = { 'CH': 'chicago.csv',
              'NY': 'new_york_city.csv',
              'WA': 'washington.csv' }

month_filter = False
day_filter = False
washington_flag = False

months=["january", "february", "march", "april", "may", "june", "all"]
days=["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "all"]

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    global month_filter
    global day_filter
    global washington_flag
    
    washington_flag = False
    month_filter = False
    day_filter = False
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city=input('Enter a city of choice out of {CH/NY/WA} to choose {Chicago/New York/Washington} respectively \n').upper()
    while city != "CH" and city != "NY" and city != "WA":
        city=input('Invalid input, enter a city of choice out of "CH/NY/WA" to choose "Chicago/New York/Washington" respectively \n').upper()
    if city == "WA":
        washington_flag = True
    # TO DO: get user input for month (all, january, february, ... , june)
    month=input('Enter a month of choice out of {January/February/March/April/May/June} or "all" to view statistics for all months from Jan to Jun \n').lower()
    
    while month.lower() not in months:
        month=input('Invalid input, enter a month of choice out of {January/February/March/April/May/June} or "all" to view statistics for all months from Jan to Jun \n')
    if month.lower() == 'all':
        month_filter=True 
        
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day=input('Enter a day of choice out of {Sunday/Monday/Tuesday/Wednesday/Thursday/Friday/Saturday} or "all" to view statistics for all days in a week \n').lower()
    while day.lower() not in days:
        day=input('Invalid input, enter a month of choice out of {Sunday/Monday/Tuesday/Wednesday/Thursday/Friday/Saturday} or "all" to view statistics for all days in a week \n')
    if day.lower() == 'all':
        day_filter=True
        
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
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month)+1
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

    # TO DO: display the most common month
    if month_filter:
        print("The most common month(s) is(are) {}".format(months[(df['month'].mode()[0])-1]))
        #print("The most common month is {}".format(df['month'].mode()[0]))

    # TO DO: display the most common day of week
    if day_filter:
        print("The most common day(s) is(are) {}".format(df['day_of_week'].mode()[0]))
    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print("The most common start hour(s) is(are) {}".format(df['hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print("The most commonly used start station(s) is(are) {}".format(df['Start Station'].mode()[0]))

    # TO DO: display most commonly used end station
    print("The most commonly used end station(s) is(are) {}".format(df['End Station'].mode()[0]))

    # TO DO: display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'] + " --> " + df['End Station']
    print("The most frequent combination(s) of start station and end station is(are) {}".format(df['Trip'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print("The total travel time is {}".format(df['Trip Duration'].sum()))

    # TO DO: display mean travel time
    print("The mean travel time is {}".format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print("The counts of user types are \n{}".format(df['User Type'].value_counts()))

    # TO DO: Display counts of gender
    if not washington_flag:
        print("The counts of users' genders are \n{}".format(df['Gender'].value_counts()))

    # TO DO: Display earliest, most recent, and most common year of birth
    if not washington_flag:
        print("The earliest year of birth is {}".format(int(df['Birth Year'].min())))
        print("The most recent year of birth is {}".format(int(df['Birth Year'].max())))
        print("The most common year(s) of birth is(are) {}".format(int(df['Birth Year'].mode()[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        counter = 0
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        raw_data = input("\nWould you like to see the raw data from the choosen city?(yes/no)\n").lower()
        while raw_data != 'yes' and raw_data != 'no':
            raw_data = input("\nInvalid input, try again.\nWould you like to see the raw data from the choosen city?(yes/no)\n").lower()
        
        while raw_data == 'yes':
            print(df.iloc[counter*5:(counter+1)*5])
            counter += 1
            raw_data = input("\nWould you like to see the raw data from the choosen city?(yes/no)\n").lower()
            while raw_data != 'Y' and raw_data != 'N':
                raw_data = input("\nInvalid input.\nWould you like to see the raw data from the choosen city?(yes/no)\n").lower()
                
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
