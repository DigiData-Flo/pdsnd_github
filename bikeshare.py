import time
import sys
from pprint import pprint
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
MONTH_DATA = {'january': 1,
              'february': 2,
              'march': 3,
              'april': 4,
              'may': 5,
              'june': 6,
              'july': 7,
              'august': 8,
              'september': 9,
              'october': 10,
              'november': 11,
              'december': 12
              }
DAY_DATA = {'monday': 0,
            'tuesday': 1,
            'wednesday': 2,
            'thursday': 3,
            'friday': 4,
            'saturday': 5,
            'sunday': 6}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filt by, or "all" to apply no month filt
        (str) day - name of the day of week to filt by, or "all" to apply no day filt
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    day = ''
    filt = ''
    time_filt = ['Month', 'Day', 'Both', 'No']

    '''Outer try block to catch different keyboard interruptions'''
    try:
        city = ''
        month = ''
        while city not in CITY_DATA:

            print('Please select one of the following cities.')
            print('Washington, Chicago, New York City')
            city = input("Please enter the city you wish to analyse: ").lower()

            if city not in CITY_DATA:
                print('Unknown city')
                print('Please try again or break the program with command+D')

        while filt not in time_filt:
            print('Do you want to use a time filter?')
            print('Please choose one of the following filters.')
            print('Month, Day, Both or No for no filter')
            filt = input('Your filt please: ').title()

            if filt not in time_filt:
                print('Unknown Filter')
                print('Please try again or break the program with command+D')

        if filt == 'Both':
            while month not in MONTH_DATA:
                month = input("Please enter one month from January to June and press enter: ").lower()
                if month not in MONTH_DATA:
                    print('Unknown month')
                    print('Please try again or break the program with command+D')
            while day not in DAY_DATA:
                day = input("Please enter a weekday and press enter: ").lower()
                if day not in DAY_DATA:
                    print('Unknown weekday')
                    print('Please try again or break the program with command+D')

        if filt == 'Month':
            while month not in MONTH_DATA:
                month = input("Please enter one month from January to June and press enter: ").lower()
                if month not in MONTH_DATA:
                    print('Unknown month')
                    print('Please try again or break the program with command+D')

        if filt == 'Day':
            while day not in DAY_DATA:
                day = input("Please enter a weekday and press enter: ").lower()
                if day not in DAY_DATA:
                    print('Unknown weekday')
                    print('Please try again or break the program with command+D')

    except EOFError:
        print('Program is terminated by command D')
        sys.exit(1)
    except KeyboardInterrupt:
        print('\nProgram is terminated by keyboard interrupt')
        sys.exit(1)

    print('-'*40)
    return city, month, day, filt


def load_data(city, month=None, day=None):
    """
    Loads data for the specified city and filts by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filt by, or "all" to apply no month filt
        (str) day - name of the day of week to filt by, or "all" to apply no day filt
    Returns:
        df - Pandas DataFrame containing city data filted by month and day
    """
    '''Read csv file'''
    df_raw = pd.read_csv(CITY_DATA[city])

    '''Convert Time columns to Date Time objects'''
    df_raw['Start Time'] = pd.to_datetime(df_raw['Start Time'])
    df_raw['End Time'] = pd.to_datetime(df_raw['End Time'])

    '''Add Date Time columns and a Trip columns to Dataframe'''
    df_raw['Week Day'] = df_raw['Start Time'].dt.day_name()
    df_raw['Month'] = df_raw['Start Time'].dt.month_name()
    df_raw['Hour'] = df_raw['Start Time'].dt.hour
    df_raw['Trip'] = df_raw['Start Station'] + ', ' + df_raw['End Station']

    print('The selected filter is: ', month, day)
    if month and day:
        df = df_raw[df_raw['Month'] == month.title()]
        df = df[df_raw['Week Day'] == day.title()]
    elif month:
        df = df_raw[df_raw['Month'] == month.title()]
    elif day:
        df = df_raw[df_raw['Week Day'] == day.title()]
    else:
        df = df_raw

    return df


def time_stats(df, filt):
    """Displays statistics on the most frequent times of travel."""

    def get_time_str(seconds):
        """
        Takes a time in seconds
        """
        minutes = int(seconds // 60)
        sec = int(seconds % 60)
        time_str = '{} min {} sec'.format(minutes, sec)
        return time_str

    def get_popular_time(df, time_label):
        """
        takes a Dataframe and a time label ('Month' or 'Day')

        returns most and least popular time stamp for the given label
        returns the corresponding counts for the time stamps
        return the results as a dictionary
        """
        label = time_label.title()

        try:
            max_value = df[label].value_counts().idxmax()
            min_value = df[label].value_counts().idxmin()
        except ValueError:
            max_value = None
            min_value = None

        popularity_dict = {
            'max_{}'.format(time_label.lower()): max_value,
            'max_count': df[label].value_counts().max(),
            'min_{}'.format(time_label.lower()): min_value,
            'min_count': df[label].value_counts().min()
        }

        return popularity_dict

    print('\nCalculating The Most Frequent Times of Travel...\n')


    start_time = time.time()

    '''For No filt calculate the popular month and day'''
    if filt == 'No':
        label = 'Month'
        pop_dict = get_popular_time(df, label)

        max_month = pop_dict['max_month']
        min_month = pop_dict['min_month']

        max_str = 'The most popular {} is {} with {} trips'.format(
            label.lower(),  # month, day
            pop_dict['max_{}'.format(label.lower())],  # max_month, max_day
            pop_dict['max_count'])
        min_str = 'The least popular {} is {} with {} trips'.format(
            label.lower(),  # month, day
            pop_dict['min_{}'.format(label.lower())],  # max_month, max_day
            pop_dict['min_count'])

        print(max_str)
        print(min_str)

        label = 'Week Day'
        pop_dict = get_popular_time(df, label)

        max_str = 'The most popular {} is {} with {} trips'.format(
            label.lower(),  # month, day
            pop_dict['max_{}'.format(label.lower())],  # max_month, max_day
            pop_dict['max_count'])
        min_str = 'The least popular {} is {} with {} trips'.format(
            label.lower(),  # month, day
            pop_dict['min_{}'.format(label.lower())],  # max_month, max_day
            pop_dict['min_count'])

        print(max_str)
        print(min_str)

        avg = get_time_str(df.groupby('Month').mean().loc[max_month]['Trip Duration'].mean())
        print('Average Trip Duration in the month {} with highest rental counts is'.format(max_month), avg, '.')

        avg = get_time_str(df.groupby('Month').mean().loc[min_month]['Trip Duration'].mean())
        print('Average Trip Duration in the month {} with lowest rental counts is'.format(min_month), avg, '.')

    '''For Month filt calculate the popular month and day'''
    if filt == 'Month':

        label = 'Week Day'
        pop_dict = get_popular_time(df, label)

        max_str = 'The most popular {} is {} with {} trips'.format(
            label.lower(),  # month, day
            pop_dict['max_{}'.format(label.lower())],  # max_month, max_day
            pop_dict['max_count'])
        min_str = 'The least popular {} is {} with {} trips'.format(
            label.lower(),  # month, day
            pop_dict['min_{}'.format(label.lower())],  # max_month, max_day
            pop_dict['min_count'])

        print(max_str)
        print(min_str)

        label = 'Hour'
        pop_dict = get_popular_time(df, label)

        max_str = 'The most popular {} is {} with {} trips'.format(
            label.lower(),  # month, day
            pop_dict['max_{}'.format(label.lower())],  # max_month, max_day
            pop_dict['max_count'])
        min_str = 'The least popular {} is {} with {} trips'.format(
            label.lower(),  # month, day
            pop_dict['min_{}'.format(label.lower())],  # max_month, max_day
            pop_dict['min_count'])
        print(max_str)
        print(min_str)


        avg = get_time_str(df['Trip Duration'].mean())
        print('Average Trip Duration is', avg,'.')

    '''For Week Day filt calculate the popular month and day'''
    if filt == 'Day':

        label = 'Month'
        pop_dict = get_popular_time(df, label)

        max_str = 'The most popular {} is {} with {} trips'.format(
            label.lower(),  # month, day
            pop_dict['max_{}'.format(label.lower())],  # max_month, max_day
            pop_dict['max_count'])
        min_str = 'The least popular {} is {} with {} trips'.format(
            label.lower(),  # month, day
            pop_dict['min_{}'.format(label.lower())],  # max_month, max_day
            pop_dict['min_count'])

        print(max_str)
        print(min_str)

        label = 'Hour'
        pop_dict = get_popular_time(df, label)

        max_str = 'The most popular {} is {} with {} trips'.format(
            label.lower(),  # month, day
            pop_dict['max_{}'.format(label.lower())],  # max_month, max_day
            pop_dict['max_count'])
        min_str = 'The least popular {} is {} with {} trips'.format(
            label.lower(),  # month, day
            pop_dict['min_{}'.format(label.lower())],  # max_month, max_day
            pop_dict['min_count'])
        print(max_str)
        print(min_str)

        avg = get_time_str(df['Trip Duration'].mean())
        print('Average Trip Duration is', avg, '.')


    '''For Both filt calculate the popular month and day'''
    if filt == 'Both':

        avg = get_time_str(df['Trip Duration'].mean())
        print('Average Trip Duration is', avg, 'minutes')

        label = 'Hour'
        pop_dict = get_popular_time(df, label)

        max_str = 'The most popular {} is {} with {} trips'.format(
            label.lower(),  # month, day
            pop_dict['max_{}'.format(label.lower())],  # max_month, max_day
            pop_dict['max_count'])
        min_str = 'The least popular {} is {} with {} trips'.format(
            label.lower(),  # month, day
            pop_dict['min_{}'.format(label.lower())],  # max_month, max_day
            pop_dict['min_count'])
        print(max_str)
        print(min_str)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):

    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    df_start_station = pd.DataFrame(df['Start Station'].value_counts())
    df_end_station = pd.DataFrame(df['End Station'].value_counts())
    df_station = df_start_station.merge(df_end_station, how='outer', left_index=True, right_index=True)

    start_station_count = df['Start Station'].value_counts().count()
    end_station_count = len(df['End Station'].value_counts())
    station_count_str = 'There are {} start stations and {} end stations in the dataset' \
        .format(start_station_count, end_station_count)
    print(station_count_str,'\n')

    df_station['Start Station'].sort_values(ascending=False)
    popular_start = df_station['Start Station'].idxmax()
    popular_departure = df_station['Start Station'].max()
    popular_arrival = str(df_station.loc[popular_start]['End Station'])
    if popular_arrival == 'nan':
        popular_arrival = 0

    start_station_str = 'The most popular start station is {} with {} starts at this station and {} \
ends at this station'.format(popular_start, popular_departure, popular_arrival)
    print(start_station_str, '\n')

    df_station['End Station'].sort_values(ascending=False)
    popular_end = df_station['End Station'].idxmax()
    popular_arrival = df_station['End Station'].max()
    popular_departure = str(df_station.loc[popular_end]['Start Station'])
    if popular_departure == 'nan':
        popular_departure = 0
    start_station_str = 'The most popular end station is {} with {} arrives at this station and {} \
starts from this station'.format(popular_end, popular_arrival, popular_departure)
    print(start_station_str, '\n')

    df_station.fillna(0, inplace=True)
    df_station['Difference'] = df_station['End Station'] - df_station['Start Station']
    total_station_count = len(df_station)
    surplus = (df_station['Difference'] > 0).sum()
    deficit = (df_station['Difference'] < 0).sum()
    equality = (df_station['Difference'] == 0).sum()

    explanation_str = 'Let\'s assume, that a start station can also be a end station. \n\
In total there are {} stations in the datasets independent is it a \
start or an end or a both station is.\nFor many stations we get a bike surplus \
or a bike deficit.'.format(total_station_count)
    surplus_str = 'For {} stations we get a bike surplus and for {} stations we get a bike deficit \
and for {} stations the arrival and departure values are equal.'.format(surplus, deficit, equality)

    print(explanation_str, '\n')
    print(surplus_str)

    trip_count = df['Trip'].value_counts().count()
    trip_count_str = 'There are {} different trips in the dataset'.format(trip_count)
    print(trip_count_str, '\n')

    df_trip = pd.DataFrame(df['Trip'].value_counts())
    df_trip.rename(columns={'Trip': 'Trip Count'}, inplace=True)
    trip_larger_1 = df_trip[df_trip['Trip Count'] > 1].count()[0]
    trip_times_max = df_trip[df_trip['Trip Count'] > 1].max()[0]
    if trip_larger_1 > 1:
        trip = df_trip[df_trip['Trip Count'] > 1].idxmax()[0]
    else:
        trip_times_max = 1
        trip = 'any trip'

    trip_str = 'There are {} trips which occurs more than one time in the dataset. The maximum trip count is {} \
for the trip {}. Below there are the top 5 trips and the occurences.' \
        .format(trip_larger_1, trip_times_max, trip)

    print(trip_str, '\n')

    print(df_trip.head(5))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    if 'Gender' in df.columns:
        total_count = len(df)
        no_count = df['Gender'].isnull().sum()
        male_count = len(df[df['Gender'] == 'Male'])
        female_count = len(df[df['Gender'] == 'Female'])

        ratio_no = round(no_count / total_count * 100, 2)
        ratio_male = round(male_count / total_count * 100, 2)
        ratio_female = round(female_count / total_count * 100, 2)

        gender_str = 'There are {}% female user, {}% male user and {}% with no gender information' \
            .format(ratio_female, ratio_male, ratio_no)

        print(gender_str)

        df_male = df[df['Gender'] == 'Male']
        male_mean = round(df_male['Birth Year'].mean(), 2)
        male_std = round(df_male['Birth Year'].std(), 2)

        df_female = df[df['Gender'] == 'Female']
        female_mean = round(df_female['Birth Year'].mean(), 2)
        female_std = round(df_female['Birth Year'].std(), 2)

        gender_birth_str = 'The mean birth year of female user is {},\n\
The mean birth year of male user is {}.\n\
The standard deviation of female user is {}.\n\
The standard deviation of male user is {}.' \
.format(female_mean, male_mean, female_std, male_std)

        print(gender_birth_str)

    else:
        subscriber = len(df[df['User Type'] == 'Subscriber'])
        customer = len(df[df['User Type'] == 'Customer'])

        user_str = 'There are {} subscriber and {} customer in the dataset'.format(subscriber, customer)
        print(user_str)




    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day, filt = get_filters()

        if filt == 'Both':
            print('Selected city: {}\nSelected month: {}\nSelected day: {}\nSelected filter: {}'\
                  .format(city, month, day, filt))
            df = load_data(city, month=month, day=day)
        elif filt == 'Month':
            print('Selected city: {}\nSelected month: {}\nSelected filter: {}'.format(city, month, filt))
            df = load_data(city, month=month)
        elif filt == 'Day':
            df = load_data(city, day=day)
            print('Selected city: {}\nSelected day: {}\nSelected filter: {}'.format(city, day, filt))
        else:
            print('Selected city: {}'.format(city, filt))
            df = load_data(city)

        if len(df) == 0:
            print('The Dataframe is empty, please try another configuration')
            continue

        print('Dataframe overview')
        pprint(df.head(3).to_dict(orient='index'))

        time_stats(df, filt)
        station_stats(df)
        user_stats(df)

        i = 0
        while True and i < len(df):

            raw_data = input('\nWould you like to see raw data? Enter yes or no.\n')

            if raw_data.lower() != 'yes':
                break

            pprint(df[i:i+5].to_dict(orient='index'))
            i = i + 5



        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()

