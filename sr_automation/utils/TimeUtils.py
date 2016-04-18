import time
import os
from datetime import datetime

from logbook import Logger
log = Logger("TimeUtils")


class TimeUtils(object):
    
    @staticmethod
    def sync_time():
        os.system('adb shell date -s '+datetime.now().strftime("%Y%m%d.%H%M%S"))

    @staticmethod
    def format_time(i_unformattedTime):
        toFormat = str(datetime.now().day) + "-" + str(datetime.now().month) + "-" + str(datetime.now().year) + " " + i_unformattedTime[0] + ":" + i_unformattedTime[1]
        if i_unformattedTime[2] == 'p':
            toFormat += "PM"
        else:
            toFormat += "AM"
        strippedTime = datetime.strptime(toFormat,'%d-%m-%Y %I:%M%p')
        return strippedTime.time()
    
    @staticmethod
    def get_next_interval():
        currentHour = int(datetime.now().hour)
        currentMinute = int(datetime.now().minute)
        if currentMinute > 55:
            if currentHour < 12:
                timeToSet = [str(currentHour+1),'0','a']
            elif currentHour > 12:
                timeToSet = [str(currentHour-12),'0','p']
            else:
                timeToSet = ['1','0','p']
        else:
            if currentHour <=12:
                timeToSet = [str(currentHour),str(currentMinute+3),'a']
            else:
                timeToSet = [str(currentHour-12),str(currentMinute+3),'p']
        if timeToSet[1] > 10:
            ones = int(timeToSet[1][1])
            tens = int(timeToSet[1][0]) * 10
        else:
            ones = int(timeToSet[1][0])
            tens = 0
        if ones < 8:
            ones += 2
        else:
            tens += 10
            ones = 0
        timeToSet[1] = str(tens + ones)
        return timeToSet
