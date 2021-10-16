import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

# define the 3 lists to be used in the function
cities_list = ['chicago', 'new york city', 'washington']
month_list = ['January', 'February', 'March', 'April', 'May', 'June', "All"]
day_list = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'All']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    # note : I use numbers 1,2,3 in while loop as an 'always true' condition with a break when condition is met
    # while loops are here for the input of the user and to check if they are valid or not
    # if user's answer is not in the list:
    #           it will show error message and keep asking the user until he gives a valid answer
    while 1:
        city_input = input('which city would you like to see data from? please choose from the list below ▼: \nChicago\nNew York\nWashington\n').lower()
        # we lower format the var city to match what's in cities_list and the dictionary keys in CITY_DATA as well
        city = city_input
        if city in cities_list:
            break
        elif city == 'new york':
            city = 'new york city'
            break
        else:
            print('*- Wrong City Name -*')
    while 2:
        month_input = input('which Month would you like to see data from? please choose from the list below ▼:\n'
                            'January     April\nFebruary    May\nMarch       June\n       All\n').title()
        month = month_input
        if month in month_list:
            break
        else:
            print('*- Wrong Month Name')
    while 3:
        day_input = input('which Day would you like to see data from ? please choose from the list below  ▼ :\n'
                          'Sunday     Thursday\nMonday     Friday\nTuesday    Saturday\nWednesday  All\n').title()
        day = day_input
        if day.title() in day_list:
            break
        else:
            print('*- Wrong Day Name -*')
    print('-' * 40,'\nlooding please wait...')
    return city, month, day


def load_data(city , month , day):
    """
      Loads data for the specified city and filters by month and day if applicable.

      Args:
          (str) city - name of the city to analyze
          (str) month - name of the month to filter by, or "all" to apply no month filter
          (str) day - name of the day of week to filter by, or "all" to apply no day filter
      Returns:
          df - Pandas DataFrame containing city data filtered by month and day
      """
    # getting the data from the dictionary with the data returned by function get_fliters
    df = pd.read_csv(CITY_DATA[city])
    # cleaning the data and adding  colunms  in the below steps
    #  renaming the empty first label  to Trip ID
    df = df.rename(columns={df.columns[0]: 'Trip ID'})
    #  changing the format of Start Time from object to datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    #  adding new column with label (Hour, day,month number, month name,week name
    df['Hour'] = pd.DatetimeIndex(df['Start Time']).hour
    df['Day'] = pd.DatetimeIndex(df['Start Time']).day
    df['Month_numb'] = pd.DatetimeIndex(df['Start Time']).month
    df['Month_name'] = df['Start Time'].dt.month_name()
    df['dayOfWeek'] = df['Start Time'].dt.day_name()
    # used try  and exception  to add 'Birth Year' column in Washington
    try:
        #  changing birth date from  float64 to datetime
        df['Birth Year'] = pd.to_datetime(df['Birth Year'], format='%Y')
        #  changing birth date from  datetime to a period
        df['Birth Year'] = df['Birth Year'].dt.to_period('y')
    except KeyError:
        pass
    #  creating a new column to combine start and end stations
    df['start_end'] = df['Start Station'] + ' ===>>' + df['End Station']

    # created new lists  monthz & dayz lists in lines 93, 101 for the day and months without (all)
    monthz_list = ['January', 'February', 'March', 'April', 'May', 'June']
    # useing for loop to iterate throw the above  lists
    for monthz in monthz_list:
        # checking if monthz match user input
        if monthz == month:
            # creating DataFrame with the filtered month according to user input
            df = df[df['Month_name'] == month]
        else:
            # when the user input not in the list df will remain the same in the line 67
            break
    dayz_list = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    for dayz in dayz_list:
        if dayz == day:
            df = df[df['dayOfWeek'] == day]
        else:
            break
    return df


# I use the tag '# extra' in the comments below when something was not requested in the project
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    # there are methods to get most frequent like  mode() or value_counts().idxmax() but with mode we get dtype: object after the print
    cmn_month = df['Month_name'].value_counts().idxmax()
    # extra
    count_month = df['Month_name'].value_counts().max()
    cmn_week = df['dayOfWeek'].value_counts().idxmax()
    # extra
    count_week = df['dayOfWeek'].value_counts().max()
    cmn_hour = df['Hour'].value_counts().idxmax()
    # extra
    count_hour = df['Hour'].value_counts().max()
    # TO DO: display the most common month
    print('- Most common month was {}'.format(cmn_month), '\n-',cmn_month,'appeared {}'.format(count_month),' times.')
    # TO DO: display the most common day of week
    print('- Most Common Day of Week',cmn_week,'\n-',cmn_week,' appeared' ,count_week,' times.')
    # TO DO: display the most common start hour
    print('- Most Common Hour of day','(',cmn_hour,')\n- the hour (',cmn_hour,') appeared',count_hour,' times.')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    cmn_start = df['Start Station'].value_counts().idxmax()
    count_start = df['Start Station'].value_counts().max()
    print('- Most Common Start Station',cmn_start,'\n-',cmn_start ,' Station appeared ' ,count_start, ' times.')
    # TO DO: display most commonly used end station
    cmn_end = df['End Station'].value_counts().idxmax()
    # extra
    count_end = df['End Station'].value_counts().max()
    print('- Most Common End Station ',cmn_end,'\n-',cmn_end ,' Station appeared ',count_end,' times.')
    # TO DO: display most frequent combination of start station and end station trip
    cmn_startend = df['start_end'].value_counts().idxmax()
    # extra
    count_startend = df['start_end'].value_counts().max()
    print('- Most Common Trip from start to end are ',cmn_startend,'\n-',cmn_startend,' Station appeared ',count_startend,' times.')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_trip_time = df['Trip Duration'].sum()
    print('- Total Trip Time by Hours   = ', (total_trip_time/60/60),'Hours')

    # TO DO: display mean travel time
    average_t_time = df['Trip Duration'].mean()
    print('- Average Trip Time by minutes = ', int(average_t_time/60),'Minutes')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print('- User Types\n{}'.format(user_types))
    # TO DO: Display counts of gender
    try:
        gender_types = df['Gender'].value_counts()
        print('- Gender Type\n{}'.format(gender_types))
    except KeyError:
        print('- Gender statistics are not available for the choosen city')

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        earliest = df['Birth Year'].min()
        most_recent = df['Birth Year'].max()
        most_common = df['Birth Year'].value_counts().idxmax()
        print('- Earliest customer year of birth is {}'.format(earliest))
        print('- Most recent customer year of birth is {}'.format(most_recent))
        print('- Most common customer year of birth is  {}'.format(most_common))
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
    except KeyError:
        print('- Year of birth statistics are not available for the choosen city')



def show_data(df):
    valid_data = input("Would you like to view 5 rows of individual trip data? Enter yes or no?").lower()
    start_loc = 0
    while True:
        if valid_data == 'no' :
            break
        elif  valid_data == 'yes' :
            print(df.iloc[start_loc:start_loc + 5])
            start_loc += 5
            valid_data = input("Do you wish to continue?: ").lower()
        else :
            print('not valid input')
            valid_data = input("please Enter yes or no?").lower()



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
