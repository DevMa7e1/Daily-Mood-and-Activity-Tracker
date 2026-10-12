import ttkbootstrap as ttk
from tkinter import HORIZONTAL, END, Variable
import tkinter.font as tkFont
from record import write_down, read_back, modify, read_relevant_events, read_all_events
from datetime import datetime
from classes import Day, Global
from math import floor
from tkcalendar import Calendar
from tk_classes import EventList, MessageBox

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
    MessageBox().show_message('Done', 'Information recorded!')

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
    cal = Calendar(dt_frame, date_pattern='yyyy/MM/dd', selectmode="day", year=datetime.now().year, month=datetime.now().month, day=datetime.now().day,
        showweeknumbers=False, firstweekday="monday",
        background="#FFCD39", foreground="#000000",
        headersbackground="#FFB923", selectbackground="#FFDD77", selectforeground="white")
    cal.pack(padx=4, pady=4)
    time = ttk.Frame(dt_frame)
    t1 = ttk.Spinbox(time, bootstyle='primary', from_=0, to=23, width=2).grid(row=0, column=0)
    t1.insert(END, '12')
    ttk.Label(time, text=':').grid(row=0, column=1)
    t2 = ttk.Spinbox(time, bootstyle='primary', from_=0, to=60, width=2).grid(row=0, column=2)
    t2.insert(END, '30')
    time.pack(anchor='w', padx=4)
    dt_frame.pack(padx = 5, pady = 5)
    
    raw = read_relevant_events()
    ev = []
    for i in raw.keys():
        ev.append((raw[i], i))
    ev.sort(key=lambda e: e[0], reverse=True)
    ev = Global(ev)
    events = ["No events"]
    for i in ev.get():
        events.append(f'{i[1]}')
    if len(events) > 1:
        events = events[1:]
    dates = []
    for i in ev.get():
        dates.append(i[0])

    add_frame.grid(row=0, column=0, padx=4, pady=4)

    remove_frame = ttk.Frame(window, relief='raised', padding=2, borderwidth=1)
    remove_frame.grid_columnconfigure(0, weight=1)
    search = ttk.Frame(remove_frame)
    ttk.Label(search, text='Search: ').grid(row=0, column=0, padx=(4, 0), pady=(4, 0))
    sv = Variable(window)
    ttk.Entry(search, bootstyle='warning', textvariable=sv).grid(row=0, column=1, padx=(0, 4), pady=(4, 0))
    search.grid(pady=(0, 4), row=0, column=0, sticky='w')
    canvas = ttk.Canvas(remove_frame, width=350, height=335)
    
    scrollbar = ttk.Scrollbar(remove_frame, orient="vertical", command=canvas.yview)
    scrollbar.grid(row = 1, column = 1, sticky='ns')
    
    canvas.configure(yscrollcommand=scrollbar.set)
    listbox = EventList(canvas, events, dates, ev)
    sv.trace_add('write', lambda a, b, c: search_list(ev, sv.get(), listbox))
    ttk.Button(add_frame, text='Write down', bootstyle='danger outline', command=\
    lambda: writedownevent(name, t1, t2, cal, listbox, ev)).pack(anchor='e', padx=5, pady=5)
    canvas.create_window((0, 0), window=listbox.frame, anchor="n", width=350)
    listbox.frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.grid(row=1, column=0, sticky='e')
    remove_frame.grid(row=0, column=1, sticky='nsew', padx=4, pady=4)

def search_list(ev: Global, text: str, listbox: EventList):
    ev2 = []
    dates2 = []
    for i in ev.get():
        if text.lower() in i[1].lower():
            ev2.append(i)
    events2 = ["No events"]
    for i in ev2:
        events2.append(f'{i[1]}')
        dates2.append(i[0])
    if len(events2) > 1:
        events2 = events2[1:]
    listbox.events = events2
    listbox.dates = dates2
    listbox.update()
    

def writedownevent(name: ttk.Entry, time1: ttk.Spinbox, time2: ttk.Spinbox, calendar: Calendar, listbox: EventList, ev: Global):
    n = name.get()
    hour = int(time1.get())
    minute = int(time2.get())
    date = datetime(int(calendar.get_date().split('/')[0]), int(calendar.get_date().split('/')[1]), int(calendar.get_date().split('/')[2]), hour, minute)
    aborted = False
    if(read_back(date) == False):
        write_down(Day(date, events={n: date}))
        ev2: list = ev.get()
        ev2.append((date, n))
        ev2.sort(key=lambda e: e[0], reverse=True)
        ev.set(ev2)

        events2 = []
        for i in ev.get():
            events2.append(f'{i[1]}')
        dates2 = []
        for i in ev.get():
            dates2.append(i[0])
        listbox.events = events2
        listbox.dates = dates2
        listbox.update()
    else:
        day: Day = read_back(date) #type: ignore
        events: dict = day.events
        if n in events.keys():
            if MessageBox().ask("Warning", "Writing down an activity/event with the same name\n\
as another one within the same day\nwill overwrite the first activity/event. Continue?"):
                events[n] = date
                modify(Day(date, day.rating, day.word, events))
                ev2: list = ev.get()
                for i in ev2:
                    if i[0].year == date.year and i[0].month == date.month and i[0].day == date.day and i[1] == n:
                        ev2.remove(i)
                ev2.append((date, n))
                ev2.sort(key=lambda e: e[0], reverse=True)
                ev.set(ev2)

                events2 = []
                for i in ev.get():
                    events2.append(f'{i[1]}')
                dates2 = []
                for i in ev.get():
                    dates2.append(i[0])
                listbox.events = events2
                listbox.dates = dates2
                listbox.update()
            else:
                aborted = True
        else:
            events[n] = date
            modify(Day(date, day.rating, day.word, events))
            ev2: list = ev.get()
            ev2.append((date, n))
            ev2.sort(key=lambda e: e[0], reverse=True)
            ev.set(ev2)

            events2 = []
            for i in ev.get():
                events2.append(f'{i[1]}')
            dates2 = []
            for i in ev.get():
                dates2.append(i[0])
            listbox.events = events2
            listbox.dates = dates2
            listbox.update()
    if not aborted:
        MessageBox().show_message("Done", "Information recorded!")
    else:
        MessageBox().show_message("Aborted", "Information discarded.")

def day_stats(date: datetime):
    window = ttk.Toplevel(title=str(date.date()))

    day: Day = read_back(date) #type: ignore
    ttk.Label(window, text="Day stats", font=tkFont.Font(family="Arial", size=20)).grid(row=0, column=0)
    stuff = ttk.Frame(window)
    if type(day) == Day:
        style = 'primary'
        if day.rating < 5:
            style = 'danger'
        elif day.rating > 5:
            style = 'success'
        infos = ttk.Frame(stuff)
        mood = ttk.Frame(infos)
        mood.grid_columnconfigure(0, weight=1)
        ttk.Meter(mood, bootstyle=style, amount_used=day.rating*10, show_text=False).grid(row=1, column=0)
        ttk.Label(mood, text=f' {day.rating}/10', font=tkFont.Font(family="Arial", size=15)).grid(row=2, column=0)
        mood.pack(anchor='w')
        word = ttk.Frame(infos)
        ttk.Label(word, text='„').grid(row=0, column=0)
        ttk.Label(word, text=day.word, font=tkFont.Font(family="Arial", size=16, slant='italic', weight='bold')).grid(row=0, column=1)
        ttk.Label(word, text="”").grid(row=0, column=2)
        word.pack()
        infos.grid(row=1, column=0, sticky='nsew', padx=4, pady=4)
    else:
        style = 'primary'
        infos = ttk.Frame(stuff)
        mood = ttk.Frame(infos)
        mood.grid_columnconfigure(0, weight=1)
        ttk.Meter(mood, bootstyle=style, amount_used=0, show_text=False).grid(row=1, column=0)
        ttk.Label(mood, text=f'0/10', font=tkFont.Font(family="Arial", size=15)).grid(row=2, column=0)
        mood.pack(anchor='w')
        word = ttk.Frame(infos)
        ttk.Label(word, text='No data', font=tkFont.Font(family="Arial", size=16)).grid(row=0, column=1)
        word.pack()
        infos.grid(row=1, column=0, sticky='nsew', padx=4, pady=4)

    events = ttk.Frame(stuff)
    canvas = ttk.Canvas(events, width=250, height=300)
    scrollbar = ttk.Scrollbar(events, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    if type(day) == Day:
        evdict = day.events
    else:
        evdict = {}
    ev = []
    for i in evdict.keys():
        ev.append((evdict[i], i))
    ev.sort(key=lambda e: e[0], reverse=True)
    ev = Global(ev)
    events2 = []
    dates = []
    for i in ev.get():
        events2.append(i[1])
        dates.append(i[0])
    listbox = EventList(canvas, events2, dates, ev, False)
    canvas.create_window((0, 0), window=listbox.frame, anchor="n", width=250)
    listbox.frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.pack(expand = True, fill='both')
    events.grid(row=1, column=1)
    stuff.grid(row=1, column=0)


def searchallevents():
    window = ttk.Toplevel(title='All activities/events')
    window.resizable(width=False, height=False)

    canvas = ttk.Canvas(window, width=250, height=300)
    scrollbar = ttk.Scrollbar(window, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)
    search = ttk.Frame(window)
    sv = Variable(window)
    ttk.Entry(search, bootstyle='primary', textvariable=sv).grid(row=0, column=0, padx=4, pady=4)
    ttk.Button(search, text='Search').grid(row=0, column=1, padx=(0, 4))
    search.pack()

    evdict = read_all_events()
    ev = []
    for i in evdict.keys():
        ev.append((evdict[i], i))
    ev.sort(key=lambda e: e[0], reverse=True)
    ev = Global(ev)
    events = []
    dates = []
    for i in ev.get():
        events.append(i[1])
        dates.append(i[0])
    
    listbox = EventList(canvas, events, dates, ev, False)
    sv.trace_add('write', lambda a, b, c: search_list(ev, sv.get(), listbox))
    canvas.create_window((0, 0), window=listbox.frame, anchor="n", width=250)
    listbox.frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.pack(expand = True, fill='both')
