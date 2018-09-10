import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
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
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    	        
    while True:
        city = input('Which city would you like to explore: Chicago, New York, or Washington? ')
        if city.lower() not in ('chicago', 'new york', 'washington'):
            print('You entered an invalid city name, please retry')
        else:
            break        
    
    # TO DO: get user input for month (all, january, february, ... , june)
   
    while True:
        month = input('Which month would you like data on: January, February, March, April, May, June, or All? ')
        if month.lower() not in ('january', 'february', 'march', 'april', 'may', 'june', 'all'):
            print('You entered an invalid timeframe, please retry')
        else:
            break

   
   # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Which day of the week would you like data on: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or All? ')
        if day.lower() not in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday','all'):
            print('You entered an invalid day selection, please retry')
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
    #load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city.lower()])

    #convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    #filter by month if applicable
    if month.lower() != 'all':
        #use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month.lower()) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day.lower() != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    print('Most Popular Month:', popular_month)
    
    # TO DO: display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most Popular Day:', popular_day)
    
    
    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df.hour.mode()[0]
    print('Most Popular Start Hour:', popular_hour)
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-')


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    start_station_unique = df['Start Station'].nunique()
    print ('Number of Unique Start Stations:', start_station_unique)

    print('\nThe most popular Start Station is:')
    start_station = df.groupby(['Start Station']).size().idxmax()
    print(start_station, '\n')

    
    # TO DO: display most commonly used end station
    end_station_unique = df['End Station'].nunique()
    print ('Number of Unique End Stations:', end_station_unique)
    print('\nThe most popular End Station is:')
    end_station = df.groupby(['End Station']).size().idxmax()
    print(end_station, '\n')


    # TO DO: display most frequent combination of start station and end station trip
    print('The most popular station combination is:')
    popular_station_combo = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print(popular_station_combo)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    trip_count = len(df.axes[0])    
    print('Total number of trips:', trip_count, '\n')
    total_travel_time = df['Trip Duration'].sum()
    round_total_travel_time = format((total_travel_time / 3600) / 24, '.2f')
    print('Total Travel Time in days is:', round_total_travel_time, '\n')


    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    round_mean_time = format((mean_travel_time / 60), '.2f')
    print ('Mean Travel Time in minutes is:', round_mean_time)
    print("\n\nThis took %s seconds." % (time.time() - start_time))
    print('-')


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print('User Type Breakdown:')
    print(user_types)


    # TO DO: Display counts of gender
    try:
        gender = df['Gender'].value_counts()
        print('\n\nGender Breakdown:')
        print(gender)
    except:
        print('\nSorry, no gender data is available for your selected city')

      
      
    # TO DO: Display earliest, most recent, and most common year of birth
    
    try:
        #popular birth year
        popular_birth_year = df.groupby(['Birth Year']).size().idxmax()
        rounded_birth_year = int(round(popular_birth_year))
        print('\nBirth Year Breakdown:')
        print('Most Popular Birth Year:', rounded_birth_year)
        
        
        #earliest birth year
        earliest_birth_year = df['Birth Year'].min()
        rounded_earliest_birth_year = int(round(earliest_birth_year))
        print('Earliest Birth Year:', rounded_earliest_birth_year)
          

        #most recent birth year
        latest_birth_year = df['Birth Year'].max()
        rounded_latest_birth_year = int(round(latest_birth_year))
        print('Most Recent Birth Year:', rounded_latest_birth_year, '\n')
    except:
        print('\nSorry, no birth year data is available for your selected city\n')
    
  

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        print('Below is the data for the filters you selected: \n\n', df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
