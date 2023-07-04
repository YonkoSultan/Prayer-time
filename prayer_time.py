#!/usr/bin/env python3
'''program to get a notification when prayer time comes'''

# For web
import requests, re

# For files
import sys
import os

# For notifications and other things
from plyer import notification
import time


def Errors(err, error_time):
    '''this function deal with errors and log the error if it was repeated 3 times

    for example : 

        If connection error happend, it will retry 3 times every 20 minutes
        then it will log the error and close the program.'''

    global _attempts
    _attempts += 1

    if _attempts == 3:

        try:
            print("Couldn't fix the problem, check the error log..")

            with open(error_log, 'a') as file:

                file.write(f'[ERROR] [{error_time}] -->  {err}\n\n')

                file.write(f'Error type : {type(err).__name__}\n')
                file.write(f'Line : {(sys.exc_info()[2]).tb_lineno}\n')
                file.write(f'For additional help, you can contact me at : sultanxx575@gmail.com\n')

                file.write(f"{'-'*80}\n")

            sys.exit()

        except Exception as e:
            error_time_2 = time.strftime("%Y-%m-%d %H:%M", time.localtime())  # time of the error

            print(
                f"""The program was trying to write an error to the error log but it seems that another
error appeared in the error log function, so this process has failed. These are the errors :


-    error information of the error that faced the error log function are:      

    error name : {e}
    error time : {error_time_2}
    error line : {(sys.exc_info()[2]).tb_lineno}
    error type : {type(e).__name__}

-   error information for the second error that happend somewhere that isn't in the error log function are:

    error name : {err}
    error time : {error_time}
    error type : {type(err).__name__}


    if you keep getting the same problem contact me at

    sultanxx575@gmail.com"""
            )

            sys.exit()

    else:
        time.sleep(1200)
        return main()


def PrayerNotification(name):
    '''Notifications function'''
    global _attempts

    try:

        #------------------------------------------------------------------------------
        if name == "c":  # Error in connection
            return notification.notify(
                app_name="أوقات الصلاة",
                title="أوقات الصلاة",
                message='تأكد من إتصالك بالإنترنت',
                app_icon='',  # Icon path should be determined by you
            )

        elif name == 'n':  # None or something else wrong with finding prayer times
            return notification.notify(
                app_name="أوقات الصلاة",
                title="أوقات الصلاة",
                message='هنالك مشكلة في البحث عن أوقات الصلاة',
                app_icon='',  # Icon path should be determined by you
            )

        elif name == 'w':  # wrong city name
            return notification.notify(
                app_name="أوقات الصلاة",
                title="أوقات الصلاة",
                message='هنالك خطأ, تأكد من اسم المدينة\nError, check the city name',
                app_icon='',  # Icon path should be determined by you
            )
        #------------------------------------------------------------------------------

        _attempts = 0

        if time.strftime("%A") == "Friday" and name == "الظهر":
            name = 'الجمعة'

        if name == "الضحى":  # Al duha

            time.sleep(1500)  # 20 minutes and extra 5 minutes to avoid any errors from the site

        # For the 6 prayers
        # 1- Fajir
        # 2- Al duhr (Al jumaah if it was friday)
        # 3- Al asr
        # 4- Al maghrib
        # 5- Al isha
        # 6- Al duha

        return notification.notify(
            app_name="أوقات الصلاة",
            title="أوقات الصلاة",
            message='حان الآن وقت صلاة ' + name,
            app_icon='',  # Icon path should be determined by a user
        )
    except Exception as e:
        error_time = time.strftime("%Y-%m-%d %H:%M", time.localtime())
        Errors(e, error_time)


def main():
    '''getting the time of the prayer and calling the notifications function'''
    prayers_times = {}

    try:

        response = requests.get(f'https://saudi-arabia.prayertiming.net/en/{city}')

    except Exception as e:

        error_time = time.strftime("%Y-%m-%d %H:%M", time.localtime())
        PrayerNotification('c')
        Errors(e, error_time)

    try:
        # regular expression to get the prayer times from the page
        regex = re.compile(r'<td>([0-9]{2}:[0-9]{2} (?:AM|PM))</td>')

        if regex.findall(response.text):

            response = regex.findall(response.text)

            # Assigning the prayers names as key and the times as variables
            prayers_times["الفجر"] = response[0]
            prayers_times["الضحى"] = response[1]
            prayers_times["الظهر"] = response[2]
            prayers_times["العصر"] = response[3]
            prayers_times["المغرب"] = response[4]
            prayers_times["العشاء"] = response[5]

            while True:

                for prayer in prayers_times:

                    if time.strftime("%H:%M %p") == prayers_times[prayer]:
                        # checking if the current time equals that prayer time
                        # if it does then it will call the notification function PrayerNotification()
                        PrayerNotification(name=prayer)
                        time.sleep(1200)  # let the program have a break for 30 minutes

                time.sleep(1)

    except Exception as e:

        error_time = time.strftime("%Y-%m-%d %H:%M", time.localtime())
        PrayerNotification('n')

        Errors(e, error_time)


''' cities manual : 

- makkah
- jeddah
- riyadh
- jaizan
- al kharj
- buraidah
- hafr albatin

'''

# Optional, default is makkah
city = 'makkah'  # city name, check the city manual above for more info

# Optional, default is the directory of this file

current_folder: str = re.search(r'(.+\\).+$', __file__)[1]

# Optional, default is the directory of this file

error_log: str = current_folder + 'error.log'

# these are the paths of each city in the website I get the prayer times from

cities = {
    "makkah": "c16/Makkah",  #
    "jeddah": "c13/Jeddah",
    "riyadh": "c10/Riyadh",
    "jaizan": "c12/Jaizan",
    "al kharj": "c6/Al+kharj",
    "buraidah": "c11/Buraidah",
    "hafr albatin": "c1967/Hafr+albatin"
}

try:
    city = cities[city.lower()]

except KeyError as e:

    error_time = time.strftime("%Y-%m-%d %H:%M", time.localtime())

    print(
        '''Either you entered the city name wrong or the city is not supported in the program

contact me for adding new cities or if you have any problems or questions :

Github account : https://github.com/SultanCYB
my Email account : sultanxx575@gmail.com'''
    )

    PrayerNotification('w')
    Errors(e)

    sys.exit()

# global variable
_attempts: int = 0

if __name__ == '__main__':
    main()
