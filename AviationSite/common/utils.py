# A file for global utility functions

from urllib.request import urlopen
import datetime

# gets current date/time from the web
# NOTE: may break if the website it gets the time from goes down (or changes format)
def getcurrentdate():
    res = urlopen('http://just-the-time.appspot.com/')
    result = res.read().strip()
    result_str = result.decode('utf-8')
    current_date = datetime.date(int(result_str[:4]),int(result_str[5:7]),int(result_str[8:10]))
    return current_date