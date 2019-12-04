import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
        # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = get_input('Please enter the city (Chicago, New York City, Washinton): ', CITY_DATA.keys())

    # get user input for month (all, january, february, ... , june)
    MONTH_DATA = { 'all', 'january', 'february', 'march', 'april', 'may', 'june'}
    month = get_input('Please enter the month (all, january, february, ..): ', MONTH_DATA)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    DAY_DATA= {'all', 'monday','tuesday','wednesday','thursday','friday','saturday','sunday'}
    day = get_input('Please enter the weekday (all, monday, tuesday, ..): ', DAY_DATA)

    print('-'*40)
    return city, month, day

def get_input(query, options):
    """
    deprecated! 
    a small helper function to add simple auto-complete to user input from the commandline

    Args:
        (str) query - the question to ask the user
        (set) options - the possible answers
    """
    while True:
        candidate = input(query)
        for c in options:
            if c.startswith(candidate.lower()):
                print('Selected %s' % c)
                return c
                
def get_input(query, options: set):
        """
    a small helper function to add simple auto-complete to user input from the commandline

    Args:
        (str) query - the question to ask the user
        (set) options - the possible answers
    """
    while True:
        candidate = input(query)
        filtered_set = set(filter(lambda e: e.startswith(candidate.lower()), options))
        if len(filtered_set) == 1:
            c = filtered_set.pop()
            print('Selected %s' % c)
            return c
        elif len(filtered_set) > 1:
            print('Your choice "{}" is ambiguous: {}. Please be more precise.'.format(candidate, filtered_set))
        else:
            print('Your choice "%s" does not match any known data. Please select an available dataset.' % candidate)




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
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['start hour'] = df['Start Time'].dt.hour

    # display the most common month
    print('The most common month is {}.'.format(df['month'].mode()[0]))

    # display the most common day of week
    print('The most common day of week is {}.'.format(df['day_of_week'].mode()[0]))

    # display the most common start hour
    print('The most common start hour is {}.'.format(df['start hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    df['Trip'] = df['Start Station'] + ' -> ' + df['End Station']

    # display most commonly used start station
    print('The most commonly used start station is {}.'.format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print('The most commonly used end station is {}.'.format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    print('The most frequent combination of stations is {}.'.format(df['Trip'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('The total travel time is {}.'.format(df['Trip Duration'].sum()))

    # display mean travel time
    print('The mean travel time is {}.'.format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_counts = df['User Type'].value_counts()
    print('The counts of users are as follows:')
    print(user_counts.to_string())

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts(dropna = False)
        print('The counts of genders are as follows:')
        print(gender_counts.to_string())
    else:
        print('No information on genders available.')


    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('The earliest year of birth is {:.0f}'.format(df['Birth Year'].min()))
        print('The most recent year of birth is {:.0f}'.format(df['Birth Year'].max()))
        print('The most common year of birth is {:.0f}'.format(df['Birth Year'].mode()[0]))
    else:
        print('No information on birth years available.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """
    Gives the option to iteratively display raw data\n
    does not use auto-complete!
    """
    options = {'yes', 'no'}
    cont = get_input("Would you like to see the raw data? ", options)
    index = 0
    step = 5
    while cont == 'yes':
        print(df[index:index+step].to_string())
        index += step
        cont = get_input("Would you like to inspect more data? ", options)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
