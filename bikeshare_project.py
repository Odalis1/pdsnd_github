import time
import pandas as pd
import numpy as np
import calendar

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze. Handles errors.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\n')
    print('Hello! Let\'s explore some US bikeshare data!')
    
    #Capture inputs for city, month, and day. Also, use try-except block to handle errors
    while True: 
        try:
            city = str(input('Enter the name of the city that you\'d like to explore: Chicago, New York City, or Washington. ')).strip().lower()
            while city not in ["chicago", "new york city", "washington"]:
                print('\nOops, that doesn\'t look like one of the three cities.')
                city = str(input('Try entering Chicago, New York City, or Washington.\n')).strip().lower()
            else:
                print('\n')
                break
        except (ValueError, KeyError):
                print('\nOops, that doesn\'t look like one of the three cities.')
                print('Try entering Chicago, New York City, or Washington.\n')

    while True: 
        try:
            month = str(input('Enter the name of the month that you\'d like to explore: January - June. Use "all" to see the data for all months. ')).strip().lower()
            while month not in ["january","february","march","april","may","june","all"]:
                print('\nOops, that doesn\'t look like the name of a month from January - June.')
                month = str(input('Try entering a month like January, February, etc. Or use "all" for all months.\n')).strip().lower()
            else:
                print('\n')
                break
        except (ValueError, KeyError):
                print('\nOops, that doesn\'t look like the name of a month.')
                print('Check your spelling and make sure that you\'re entering a month like January, February, etc. Or use "all" for all months.\n')
            
    while True: 
        try:
            day = str(input('Enter the day of the week that you\'d like to explore: Monday - Sunday. Use "all" to see the data for all days. ')).strip().lower()
            while day not in ["monday","tuesday","wednesday","thursday","friday","saturday","sunday","all"]:
                print('\nOops, that doesn\'t look like the name of a day of the week.')
                day = str(input('Check your spelling and make sure that you\'re entering a day like Monday, Wednesday, Friday, etc. Or use "all" for all days.\n')).strip().lower()
            else:
                print('\n')
                break
        except (ValueError, KeyError):
            print('\nOops, that doesn\'t look like the name of a day of the week.')
            print('Check your spelling and make sure that you\'re entering a day like Monday, Wednesday, Friday, etc. Or use "all" for all days.\n')

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
    df['day'] = df['Start Time'].dt.dayofweek
    df['hour'] = df['Start Time'].dt.strftime('%H').add(':00')

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # use the index of the week list to get the corresponding int
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = days.index(day)
        
        # filter by day of week to create the new dataframe
        df = df[df['day'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    
    # find the most popular month
    popular_month = df['month'].mode()[0]

    # find the most popular day of the week
    popular_day = df['day'].mode()[0]

    # find the most popular hour
    popular_hour = df['hour'].mode()[0]
   
    print('\nCalculating The Most Frequent Times of Travel...\n')

    # display the most common month
    print('Most Popular Month:', calendar.month_name[popular_month])

    # display the most common day of week
    print('Most Popular Day of the Week:', calendar.day_name[popular_day])

    # display the most common start hour
    print('Most Popular Start Hour:', popular_hour)

    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')

    # find the most commonly used start station
    popular_start = df['Start Station'].mode()[0]

    # find the most commonly used end station
    popular_end = df['End Station'].mode()[0]

    # find the most frequent combination of start station and end station trip
    popular_route = (df['Start Station'] + " to " + df['End Station']).mode()[0] 
    
    # display most commonly used start station
    print('Most Popular Start Station:', popular_start)

    # display most commonly used end station
    print('Most Popular End Station:', popular_end)

    # display most frequent combination of start station and end station trip
    print('Most Popular Route:', popular_route)

    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')

    # convert the Trip Duration column to numeric
    df['Trip Duration'] = pd.to_numeric(df['Trip Duration'])
    
    # find total travel time
    total_travel = df['Trip Duration'].sum()

    # find mean travel time
    avg_travel = df['Trip Duration'].mean()

    # display total travel time
    print('Total Travel Time:', round(((total_travel/(1000*60*60))%24),2), ' hrs')

    # display mean travel time
    print('Average Travel Time', round((avg_travel/60),2), ' mins')
    
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')

    # find counts of user types
    user_types = df['User Type'].value_counts()

    # find counts of gender
    while True:
        try:
            gender = df['Gender'].value_counts()
            break
        except KeyError:
            break

    # find earliest, most recent, and most common year of birth
    while True:
        try:
            oldest = df['Birth Year'].min()
            youngest = df['Birth Year'].max()
            common = df['Birth Year'].mode()[0]
            break
        except KeyError:
            break

    # display counts of each user type
    print('Number of Each User Type:', user_types, '\n')

    # display counts of each gender
    while True:
        try:
            print('Number of Each Gender Type:', gender, '\n')
            break
        except UnboundLocalError:
            print('Gender data isn\'t available for Washington.\n')
            break
        
    # display earliest, most recent, and most common year of birth
    while True:
        try:
            print('Oldest User Born:', int(oldest))
            print('Youngest User Born:', int(youngest))
            print('Most Common Birth Year:', int(common))
            break
        except UnboundLocalError:
            print('Birth year data isn\'t available for Washington.')
            break

    print('-'*40)

    
def raw_data(city):
    """ Displays raw data upon request """
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    # count used to show more rows of raw data
    count = 0

    # ask user if they'd like to see the raw data and display 5 rows of data each time they respond "yes"
    while True:
        show_data = str(input('\nWould you like to see the raw data? Enter yes or no.\n')).strip().lower()
        if show_data == "yes" and count == 0:
            print("first round!")
            print(df.loc[0:4])
            count = 1
            start = 5
            end = 9
        elif show_data == "yes" and count > 0:
            print("next round!")
            print(df.loc[start:end])
            start = end + 1
            end = start + 4
        else:
            break

    print('*'*40)

    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

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
