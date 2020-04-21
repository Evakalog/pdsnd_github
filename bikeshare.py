import time
import pandas as pd
import numpy as np
import calendar
import datetime
from tabulate import tabulate

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def data_range (df,column,text):
    """
    Asks user to specify the logical operator and the time range.

    Returns:
        DataFrame filtered
    """
    while True:
        try:
            print(text)
            comparison = int(input('Please select filter type:\n 1.after \n 2.before \n 3.between (start-end both inclusive) \n 4.exact \n 5.all\nPlease select the number that applies\n'))
            if comparison == 1:
                start = int(input('You selected data > x .Please specify x:\n'))
                df = df.loc[df[column].ge(start)]
            elif comparison == 2:
                end = int(input('You selected data < x .Please specify x:\n'))
                df = df.loc[df[column].lt(end)]
            elif comparison == 3:
                start = int(input('You selected y <= data <= x .Please specify y:\n'))
                end = int(input('Please specify x:\n'))
                df = df.loc[df[column].between(start,end)]
            elif comparison == 4:
                start = int(input('You selected data = x .Please specify x:\n'))
                df = df.loc[df[column].eq(start)]
            elif comparison > 5:
                print("Oops! We need a number between 1 and 5.  Try again...")
                continue
            break
        except ValueError:
            print("Oops!  That was no valid number.  Try again...")
    return df


def get_input_and_load_data():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        DataFrame with the data filtered and ready for analysis
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Which city do you want the analysis for?\n Chicago\n New York City\n or\n Washington\n').lower()
        if city in ('chicago', 'new york city', 'washington'):
            print('You chose to see data for {}!'.format(city.title()))
            break
        else:
            print('Please try again not correct input')

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    df['city']=city

    # ask user for data preview
    preview = input('\nWould you like to see the first 5 rows of the data? Enter yes or no.\n')
    n=0
    pd.set_option("display.max.columns", None)
    while True:
        if preview.lower() == 'yes':
            if n<= len(df):
                print(df[n:n+5])
                preview = input('\nWould you like to see the next 5 rows of the data? Enter yes or no.\n')
                n+=5
            else:
                print('There are no more data to preview!')
                break
        else:
            break
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday
    df['hour'] = df['Start Time'].dt.hour

    # get user input for month (all, january, february, ... , june)
    text_m = 'Do you want data for specific month(s) or overall? Please first select which comparison operator you want to apply and then select month(s) based on coresponding integer 1 - 12 (Jan=1, Dec=12)'
    df = data_range (df,'month',text_m)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    text_w = 'Do you want data for specific day(s) of week ? Please first select which comparison operator you want to apply and then select day(s) of week based on coresponding integer 0 - 6 (Mon=0, Sun=6)'
    df = data_range (df,'day_of_week',text_w)

    print('-'*40)
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('For the specified period in {} our users\' favourite month to travel is {}'.format(df['city'].unique()[0].title(), calendar.month_name[df['month'].value_counts().idxmax()]))

    # display the most common day of week
    print('And the day of the week they biking the most is {}'.format(calendar.day_name[df['day_of_week'].value_counts().idxmax()]))

    # display the most common start hour
    print('Based on our data we can also say that {} is their preferred hour to use our service'.format(df['hour'].value_counts().idxmax()))

    # print("\nThis took %s seconds." % (time.time() - start_time))
    # print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most popular start station in {} is {}'.format(df['city'].unique()[0].title(), df['Start Station'].mode()[0]))
    # TO DO: display most commonly used end station
    print('and most popular end station is {}'.format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    print('Most preferred combination from our users is starting from station {} and ending on station {}'.format( df.groupby(['Start Station', 'End Station']).size().idxmax()[0],df.groupby(['Start Station', 'End Station']).size().idxmax()[1]))


    # print("\nThis took %s seconds." % (time.time() - start_time))
    # print('-'*40)

TIME_DURATION_UNITS = (
    ('year', 60*60*24*7*30*12),
    ('month', 60*60*24*7*30),
    ('week', 60*60*24*7),
    ('day', 60*60*24),
    ('hour', 60*60),
    ('min', 60),
    ('sec', 1)
)

def human_time_duration(seconds):
    if seconds == 0:
        return 'inf'
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append('{} {}{}'.format(amount, unit, "" if amount == 1 else "s"))
    return ', '.join(parts)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('We are super excited to announce that our bikes were active in total for {}!'.format(human_time_duration(df['Trip Duration'].sum())))


    # display mean travel time
    print('Average travel time per rental is {}!'.format(human_time_duration(df['Trip Duration'].mean())))

    # print("\nThis took %s seconds." % (time.time() - start_time))
    # print('-'*40)

def pprint_df(dframe):
    return tabulate(dframe, headers='keys', tablefmt='psql', showindex=False)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # display counts of user types
    user_type = df.groupby(['User Type']).size()
    user_type_table=pd.DataFrame(dict(features=user_type.index, count=user_type.values)).sort_values(by='count', ascending=False)

    print('Number of users per User Type:\n',pprint_df(user_type_table))
# Chicago and New York City
    if df['city'].unique()[0] !='washington':
        # display counts of gender
        gender = df.groupby(['Gender']).size()
        gender_table=pd.DataFrame(dict(features=gender.index, count=gender.values)).sort_values(by='count', ascending=False)
        print('Number of users per Gender:\n',pprint_df(gender_table))
        # display earliest, most recent, and most common year of birth
        print('Our youngest user was born on {}\nOur oldest user was born on {}\nAnd the majority of our users were born on {}\n'.format(int(df['Birth Year'].min()),int(df['Birth Year'].max()), int(df['Birth Year'].mode())))


    # print("\nThis took %s seconds." % (time.time() - start_time))
    # print('-'*40)


def main():
    while True:
#         city, month, day = get_filters()
        df = get_input_and_load_data()

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
