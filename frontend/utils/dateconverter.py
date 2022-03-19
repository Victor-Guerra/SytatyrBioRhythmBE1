import datetime
import time

def convertDateToUnixDate(date):
    return time.mktime(date.timetuple())
    
def convertUnixDateToDate(unixdate):
    return datetime.datetime.fromtimestamp(unixdate)