from classes import Day
from datetime import datetime
import os
from pathlib import Path
from calendar import monthrange

scriptpath = Path(os.path.realpath(__file__))
datafile = Path.joinpath(scriptpath.parent.absolute(), '.data')

def write_down(day: Day):
    f = open(datafile, 'a')
    string = ''
    string += str(day.date.timestamp()) + ':'
    string += str(day.rating)+chr(23)
    string += day.word+chr(23)

    for i in day.events.keys():
        string += i+chr(3)+str(day.events[i].timestamp())+chr(23)
    f.write(string+'\n')

def read_back(date: datetime):
    f = open(datafile, 'r')
    r = f.read().split('\n')
    l = ''
    date = datetime(date.year, date.month, date.day)
    for line in r:
        if len(line) > 1:
            if float(line.split(':', 1)[0]) == date.timestamp():
                l = line
    if l == '':
        return False
    elements = l.split(':', 1)[1].split(chr(23))
    day = Day(date)
    day.rating = int(elements[0])
    day.word = elements[1]
    for i in range(2, len(elements)):
        if(len(elements[i].split(chr(3))) > 1):
            event, dt = elements[i].split(chr(3))
            dt = datetime.fromtimestamp(float(dt))
            day.events[event] = dt
    return day

def modify(day: Day):
    f = open(datafile, 'r')
    r = f.read().split('\n')
    for line in r:
        if len(line) > 1:
            if float(line.split(':', 1)[0]) == day.date.timestamp():
                r.remove(line)

    f.close()
    f = open(datafile, 'w')
    buffer = ''
    for line in r:
        if len(line) > 1:
            buffer += line + '\n'
    string = ''
    string += str(day.date.timestamp()) + ':'
    string += str(day.rating)+chr(23)
    string += day.word+chr(23)

    buffer += string + '\n'
    f.write(buffer)

def initialize():
    if not os.path.exists(datafile):
        f = open(datafile, 'x')
        f.close()

def read_month_ratings(date: datetime):
    f = open(datafile, 'r')
    r = f.read().split('\n')
    f.close()

    values = {}
    days = monthrange(date.year, date.month)[1]
    days = range(days+1)
    for i in days:
            values[i] = 11
    for line in r:
        if len(line) > 1:
            ldate = datetime.fromtimestamp(float(line.split(':', 1)[0]))
            if ldate.year == date.year and ldate.month == date.month:
                values[ldate.day] = int(line.split(':', 1)[1].split(chr(23), 1)[0])
    return values

def read_relevant_events():
    f = open(datafile, 'r')
    r = f.read().split('\n')
    f.close()
    date = datetime.now()
    date = datetime(date.year, date.month, date.day)

    events = {}
    for line in r:
        if len(line) > 1:
            if float(line.split(':', 1)[0]) >= date.timestamp():
                raw = line.split(':', 1)[1].split(chr(23))
                for i in range(2, len(raw)-1):
                    event, dt = raw[i].split(chr(3))
                    dt = datetime.fromtimestamp(float(dt))
                    events[event] = dt
    return events