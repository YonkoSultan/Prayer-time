#!/usr/bin/env python3
'''program to get a notification when prayer time comes'''

# For web
import requests, re

# For notifications
from plyer import notification
from time import sleep, strftime

# these are the paths of each city in the website I get the prayer times from

cities = {
    "makkah": "/c16/Makkah",  #
    "jeddah": "/c13/Jeddah",
    "riyadh": "/c10/Riyadh",
    "jaizan": "/c12/Jaizan",
    "al kharj": "/c6/Al+kharj",
    "buraidah": "/c11/Buraidah",
    "hafr albatin": "/c1967/Hafr+albatin"
}

city = 'makkah' # enter the city name

city = city.lower()

def Send(name, time):
    '''Notifications function'''
    global _attempts

    if strftime("%H:%M %p") == time:
        pass

    else:
        print('Error something is wrong with the time entered')
        return

    if name == "e":  # Error in connection
        notification.notify(
            app_name="أوقات الصلاة",
            title="أوقات الصلاة",
            message='تأكد من إتصالك بالإنترنت',
            app_icon='',  # Icon path should be determined by you
        )
        return error()

    elif name == 'n':  # None
        notification.notify(
            app_name="أوقات الصلاة",
            title="أوقات الصلاة",
            message='هنالك مشكلة في البحث عن أوقات الصلاة',
            app_icon='',  # Icon path should be determined by you
        )
        return error()

    elif name == 'wrong name':
        return notification.notify(
            app_name="أوقات الصلاة",
            title="أوقات الصلاة",
            message='هنالك خطأ, تأكد من اسم المدينة\nError, check the city name',
            app_icon='',  # Icon path should be determined by you
        )

    _attempts = 0
    # if the name isn't error or none then the tool probably worked, so here we reset attempts

    if name == "الضحى":  # Al duha (currently al duha notification is not available)

        sleep(1200)  # 20 minutes for al duha
        return notification.notify(
            app_name="أوقات الصلاة",
            title="أوقات الصلاة",
            message='اقترب وقت صلاة الضحى',
            app_icon='',  # Icon path should be determined by you
        )

    else:

        if strftime("%A") == "Friday":  # Friday prayer
            name = 'الجمعة'

        return notification.notify(
            app_name="أوقات الصلاة",
            title="أوقات الصلاة",
            message='حان الآن وقت صلاة ' + name,
            app_icon='',  # Icon path should be determined by you
        )


def main():
    '''getting information from website, the time to get a notification'''
    global city

    prayers_times = {}

    try:
        response = requests.get(f'https://saudi-arabia.prayertiming.net/en/{city}')

    except:
        Send('e', strftime("%H:%M %p"))

    else:
        # parenthesis removed
        regex = re.compile(r'<td>([0-9]{2}:[0-9]{2} (?:AM|PM))</td>')  # regular expression to get
        # the prayer times from the page

        if regex.findall(response.text):

            response = regex.findall(response.text)

            prayers_times["الفجر"] = response[0]
            # prayers_times["الضحى"] = response[1]  don't include in project
            prayers_times["الظهر"] = response[2]
            prayers_times["العصر"] = response[3]  # putting prayer times into dictionary
            prayers_times["المغرب"] = response[4]
            prayers_times["العشاء"] = response[5]

            counter = 0
            while True:
                if counter == 5:  # if Al duha notification is available make it (6)

                    counter = 0  # turning it into 0 to repeat the same cycle
                    # when it reach (5), because the prayers are (5) so there is nothing
                    # to increase for or i will get an index error

                for prayer in prayers_times:

                    if strftime("%H:%M %p") == prayers_times[prayer]:
                        # checking if the current time equals that prayer time
                        # if it does then it will call the notification function (Send)
                        Send(name=prayer, time=prayers_times[prayer].strip())

                counter += 1

                sleep(1)

        else:
            Send('n', strftime("%H:%M %p"))


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


try:
    city = cities[city]

except KeyError:

    print(
        '''Either you entered the city name wrong or the city is not supported in the program

contact me for adding new cities or if you have any problems or questions :

my Twitter account : @SultanCYB
my Email account : sultanxx575@gmail.com'''
    )
    Send('wrong name', strftime("%H:%M %p"))
    exit()

# global variable

_attempts = 0

if __name__ == '__main__':
    main()
