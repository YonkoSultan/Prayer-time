#!/usr/bin/env python3
'''program to get a notification when prayer time comes'''

# For web
import requests, re

# For notifications
import schedule
from plyer import notification
from time import sleep, strftime

cities = {
    "makkah": "/c16/Makkah",
    "jeddah": "/c13/Jeddah",
    "riyadh": "/c10/Riyadh",
    "jaizan": "/c12/Jaizan",
    "alkharj": "/c6/Al+kharj",
    "buraidah": "/c11/Buraidah",
    "hafr albatin": "/c1967/Hafr+albatin"
}

# global variables

_attempts = 0
city = 'jeddah'

try:
    city = cities[city]

except KeyError:

    print(
        '''This city is not supported
Make sure that the city name
is same as the one in the supported cities list

If it is the same, then please contact me

my Twitter account : @Sultanbazher
my Email account : sultanxx575@gmail.com'''
    )


def PrayerTime(name, time):
    '''Notifications function'''
    global _attempts

    if strftime("%H:%M") == time:
        pass

    else:
        return

    if name == "e":  # Error in connection
        notification.notify(
            app_name="أوقات الصلاة",
            title="أوقات الصلاة",
            message='تأكد من إتصالك بالإنترنت',
            app_icon='C:\\Users\\sulta\\Pictures\\icons\\moon.ico',
        )
        return error()

    elif name == 'n':  # None
        notification.notify(
            app_name="أوقات الصلاة",
            title="أوقات الصلاة",
            message='هنالك مشكلة في البحث عن أوقات الصلاة',
            app_icon='C:\\Users\\sulta\\Pictures\\icons\\moon.ico',
        )
        return error()

    _attempts = 0
    # if the name isn't error or none then the tool probably worked, so here we reset attempts

    if name == "الضحى":  # Al duha

        return notification.notify(
            app_name="أوقات الصلاة",
            title="أوقات الصلاة",
            message='اقترب وقت صلاة الضحى',
            app_icon='C:\\Users\\sulta\\Pictures\\icons\\moon.ico',
        )

    else:

        if strftime("%A") == "Friday":  # Friday prayer
            name = 'الجمعة'

        return notification.notify(
            app_name="أوقات الصلاة",
            title="أوقات الصلاة",
            message='حان الآن وقت صلاة ' + name,
            app_icon='C:\\Users\\sulta\\Pictures\\icons\\moon.ico',
        )


def convert24(time):
    '''convert to 24 hours; i didnt create it'''
    # checking if last two elements of time
    # is AM and first two elements are 12

    if time[-2:] == "AM" and time[:2] == "12":
        return "00" + time[2:-2]

    # remove the AM
    elif time[-2:] == "AM":
        return time[:-2]

    # checking if last two elements of time
    # is PM and first two elements are 12
    elif time[-2:] == "PM" and time[:2] == "12":
        return time[:-2]

    else:

        # add 12 to hours and remove PM
        return str(int(time[:2]) + 12) + time[2:6]


def main():
    '''getting information from website, converting the time to 24 hour,
scheduling the time to get a notification'''
    global city

    prayers_times = {}

    try:
        response = requests.get(f'https://saudi-arabia.prayertiming.net/en/{city}')

    except:
        PrayerTime('e')

    else:
        # parenthesis removed
        regex = re.compile(r'<td>([0-9]{2}:[0-9]{2} (?:AM|PM))</td>')

        if regex.findall(response.text):

            response = regex.findall(response.text)

            Fajir = response[0]
            # AlDuha = response[1]  don't include in project
            Dhuhur = response[2]
            Asr = response[3]
            Maghrib = response[4]
            Isha = response[5]

            # -- if strftime worked then no need for all these lines --

            prayers_times["الفجر"] = convert24(Fajir)
            # prayers_times["الضحى"] = convert24(AlDuha) don't include in project
            prayers_times["الظهر"] = convert24(Dhuhur)
            prayers_times["العصر"] = convert24(Asr)
            prayers_times["المغرب"] = convert24(Maghrib)
            prayers_times["العشاء"] = convert24(Isha)

            # -- if strftime worked then no need for all these lines --

            for prayer in prayers_times:  # try strftime

                schedule.every().day.at(
                    prayers_times[prayer].strip()
                ).do(PrayerTime, name=prayer, time=prayers_times[prayer].strip())

            while True:
                schedule.run_pending()
                sleep(1)

        else:
            PrayerTime('n')


def error():
    '''function to deal with errors'''
    global _attempts

    _attempts += 1

    if _attempts == 3:
        print("Couldn't fix the problem, closing the program..")
        exit()
        # If connection error happend, it will retry 3 times every 20 minutes
        # then it will close the program if the problem didn't get fixed.
    sleep(1200)
    return main()


if __name__ == '__main__':
    main()