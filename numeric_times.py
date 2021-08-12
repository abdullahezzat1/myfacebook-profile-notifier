import datetime
import time


def get_numeric_time(string_time: str):
    # form 1: 10 hrs, 1 hr
    if string_time.endswith('hrs') or string_time.endswith('hr'):
        hrs = int(string_time[0:-3]) * 60 * 60
        numeric_time = time.time() - hrs
        # print(numeric_time)
        return numeric_time

    # form 2: 25 mins, 1 min
    if string_time.endswith('min') or string_time.endswith('mins'):
        mins = int(string_time[0:-4]) * 60
        numeric_time = time.time() - mins
        # print(numeric_time)
        return numeric_time

    # form 3: Yesterday at 4:00 PM
    if string_time.startswith('Yesterday'):
        hrs = int(string_time[-8:-6])
        mins = int(string_time[-5:-3])
        if string_time.endswith('AM'):
            hrs = 23 - hrs
        else:
            hrs = 11 - hrs
        mins = 60 - mins
        hrs = hrs + time.localtime().tm_hour
        mins = mins + time.localtime().tm_min
        secs = 60 * 60 * hrs + 60 * mins
        numeric_time = time.time() - secs
        # print(numeric_time)
        return numeric_time

    # form 4: December 31, 2018 at 10:20 PM
    if string_time.count(',') > 0:
        string_time = string_time.replace(',', '')
        string_time = string_time.replace(':', ' ')

        l = string_time.split(' ')
        months = ['none', 'January', 'Febreuary', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December']

        if l[-1] == 'PM' and int(l[-3]) != 12:
            l[-3] = str(int(l[-3]) + 12)

        del l[-1]

        # print(l)
        time_obj = datetime.datetime(int(l[2]), months.index(
            l[0]), int(l[1]), int(l[4]), int(l[5]))

        numeric_time = time_obj.timestamp()
        # print(numeric_time)
        return numeric_time

    # form 5: August 5 at 3:10 PM
    else:
        string_time = string_time.replace(':', ' ')

        l = string_time.split(' ')
        months = ['none', 'January', 'Febreuary', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December']

        if l[-1] == 'PM' and int(l[-3]) != 12:
            l[-3] = str(int(l[-3]) + 12)

        del l[-1]

        # print(l)
        time_obj = datetime.datetime(datetime.date.today().year, months.index(
            l[0]), int(l[1]), int(l[3]), int(l[4]))

        numeric_time = time_obj.timestamp()
        # print(numeric_time)
        return numeric_time
