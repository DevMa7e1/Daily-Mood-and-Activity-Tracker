import ttkbootstrap as ttk
from tkinter import HORIZONTAL, END, Variable
import tkinter.font as tkFont
from time import sleep
from record import write_down, read_back, modify, read_relevant_events
from datetime import datetime
from classes import Day
from math import floor
from tkcalendar import Calendar

def addmood(todaysbutton):
    window = ttk.Toplevel(title="What's today's mood?")
    window.resizable(width=False, height=False)

    day = Day(datetime.now())
    if read_back(datetime.now()) != False:
        day: Day = read_back(datetime.now()) #type: ignore

    rating_frame = ttk.Frame(window, relief='solid', borderwidth=1, padding=2)
    ttk.Label(rating_frame, text="Rate this day on a scale from 0 to 10.", font=tkFont.Font(family="Arial", size=12)).pack()

    sf1 = ttk.Frame(rating_frame)

    sf2 = ttk.Frame(sf1)
    label = ttk.Label(sf2, text=f'{day.rating}/10')
    rating = ttk.Scale(sf2, from_=0, to=10, orient=HORIZONTAL, length=100, value=day.rating,\
    command=lambda val: label.config(text=str(floor(float(val)))+'/10'))
    rating.pack(anchor='w')
    label.pack(anchor='w')
    sf2.grid(row=0, column=0, sticky='w')

    sf1.columnconfigure(0, weight=1)
    sf1.columnconfigure(1, weight=1)
    sf1.rowconfigure(1, weight=1)
    ttk.Button(sf1, text='?', command=addmoodhelp, bootstyle='info outline').grid(row=0, column=1, sticky='se')
    sf1.pack(fill="both", expand=True)

    rating_frame.pack(padx=4, pady=4)

    wordframe = ttk.Frame(window, relief='solid', borderwidth=1, padding=2)
    ttk.Label(wordframe, text="One word that describes today:", font=tkFont.Font(family="Arial", size=12)).pack(anchor='w')
    word = ttk.Entry(wordframe, width=20)
    word.insert(END, day.word)
    word.pack(anchor='w', padx=4, pady=4)
    wordframe.pack(padx=4, pady=4, fill='x')

    ttk.Button(window, text='Write down', bootstyle='danger outline', command=lambda: writedownmood(rating, word, window, todaysbutton)).pack(anchor='e', padx=5, pady=5)

def addmoodhelp():
    msg = ttk.Toplevel(title="Help")
    ttk.Label(msg, text="Rating guide:", font=tkFont.Font(family="Arial", size=13)).pack(anchor='w')
    ttk.Label(msg, text="0 means extremely negative\n5 means neutral\n10 means extremely positive").pack()

def writedownmood(rating: ttk.Scale, word: ttk.Entry, window: ttk.Toplevel, todaysbutton: ttk.Button):
    if read_back(datetime.now()) == False:
        day = Day(datetime.now(), floor(float(rating.get())), word=word.get())
        write_down(day)
    else:
        day: Day = read_back(datetime.now()) #type: ignore
        day.rating = floor(float(rating.get()))
        day.word = word.get()
        modify(day)
    if floor(rating.get()) < 5:
        todaysbutton.config(bootstyle='danger')
    elif floor(rating.get()) == 5:
        todaysbutton.config(bootstyle='primary')
    elif floor(rating.get()) > 5:
        todaysbutton.config(bootstyle='success')
    window.destroy()
    show_message('Done', 'Information recorded!')

def addactivity():
    window = ttk.Toplevel(title="Manage activities/events")
    window.resizable(width=False, height=False)
    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=1)
    window.grid_rowconfigure(0, weight=1)

    add_frame = ttk.Frame(window, relief='raised', padding=2, borderwidth=1)
    ttk.Label(add_frame, text="Add an activity/event:", font=tkFont.Font(family="Arial", size=13, weight='bold')).pack(anchor='w', padx=4)
    name_frame = ttk.Frame(add_frame, relief='solid', borderwidth=1, padding=4)
    ttk.Label(name_frame, text="Name:", font=tkFont.Font(family="Arial", size=12)).pack(anchor='w')
    name = ttk.Entry(name_frame, bootstyle='primary')
    name.pack(anchor='w')
    name_frame.pack(padx = 5, pady = 5, fill='x')

    dt_frame = ttk.Frame(add_frame, relief='solid', borderwidth=1, padding=4)
    ttk.Label(dt_frame, text="Date & time:", font=tkFont.Font(family="Arial", size=12)).pack(anchor='w')
    cal = Calendar(dt_frame, selectmode="day", year=datetime.now().year, month=datetime.now().month, day=datetime.now().day,
        showweeknumbers=False, firstweekday="monday",
        background="#FFCD39", foreground="#000000",
        headersbackground="#FFB923", selectbackground="#FFDD77", selectforeground="white")
    cal.pack(padx=4, pady=4)
    time = ttk.Frame(dt_frame)
    ttk.Spinbox(time, bootstyle='primary', from_=0, to=23, width=2).grid(row=0, column=0).insert(END, '12')
    ttk.Label(time, text=':').grid(row=0, column=1)
    ttk.Spinbox(time, bootstyle='primary', from_=0, to=60, width=2).grid(row=0, column=2).insert(END, '30')
    time.pack(anchor='w', padx=4)
    dt_frame.pack(padx = 5, pady = 5)
    ttk.Button(add_frame, text='Write down', bootstyle='danger outline').pack(anchor='e', padx=5, pady=5)
    add_frame.grid(row=0, column=0, padx=4, pady=4)

    remove_frame = ttk.Frame(window, relief='raised', padding=2, borderwidth=1)
    search = ttk.Frame(remove_frame)
    ttk.Label(search, text='Search: ').grid(row=0, column=0)
    ttk.Entry(search, bootstyle='warning').grid(row=0, column=1)
    search.pack(pady=(0, 4))
    raw = read_relevant_events()
    ev = []
    for i in raw.keys():
        ev.append((raw[i], i))
    ev.sort(key=lambda e: e[0], reverse=True)
    events = ["No events"]
    for i in ev:
        events.append(i[1])
    if len(events) > 1:
        events = events[1:]
    events = Variable(value=events)
    ttk.Listbox(remove_frame, listvariable=events).pack(expand=True, fill='both')
    ttk.Button(remove_frame, bootstyle='danger outline', text="Remove").pack(fill='x')
    remove_frame.grid(row=0, column=1, sticky='nsew', padx=4, pady=4)
    
def show_message(title, text):
    msg = ttk.Toplevel(title=title)
    ttk.Label(msg, text=text, font=tkFont.Font(family="Arial", size=12)).pack(padx=3, pady=3)
    msg.update()
    sleep(1)
    msg.destroy()
