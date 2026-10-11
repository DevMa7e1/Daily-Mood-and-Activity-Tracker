import ttkbootstrap as ttk
from tkinter import HORIZONTAL, END, Variable
import tkinter.font as tkFont
from time import sleep
from record import write_down, read_back, modify, read_relevant_events
from datetime import datetime
from classes import Day, Global
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
    events = Variable(window, value=events)
    dates = Global(dates)

    ttk.Button(add_frame, text='Write down', bootstyle='danger outline', command=\
    lambda: writedownevent(name, t1, t2, cal, events, dates, ev)).pack(anchor='e', padx=5, pady=5)
    add_frame.grid(row=0, column=0, padx=4, pady=4)

    remove_frame = ttk.Frame(window, relief='raised', padding=2, borderwidth=1)
    search = ttk.Frame(remove_frame)
    ttk.Label(search, text='Search: ').grid(row=0, column=0, padx=(4, 0), pady=(4, 0))
    sv = Variable(window)
    ttk.Entry(search, bootstyle='warning', textvariable=sv).grid(row=0, column=1, padx=(0, 4), pady=(4, 0))
    search.pack(pady=(0, 4))

    sv.trace_add('write', lambda a, b, c: search_list(ev, events, sv.get(), dates))
    listbox = ttk.Listbox(remove_frame, listvariable=events).pack(expand=True, fill='both', padx=4, pady=4)
    ttk.Button(remove_frame, bootstyle='danger outline', text="Remove",\
    command= lambda: remove_event(listbox, events, dates, ev)).pack(fill='x')
    remove_frame.grid(row=0, column=1, sticky='nsew', padx=4, pady=4)

def remove_event(listbox: ttk.Listbox, events: Variable, dates: Global, ev: Global):
    if len(listbox.curselection()) > 0:
        if ask("Wait", "Proceed with removing event(s)?"):
            eve: list = list(events.get())
            dat: list = list(dates.get())
            ev2: list = list(ev.get())
            for i in listbox.curselection():
                day: Day = read_back(dat[i]) #type: ignore
                day.events.pop(eve[i])
                modify(day)
                dat.pop(i)
                eve.pop(i)
            events.set(eve)
            dates.set(dat)
            ev.set(ev2)
            show_message("Done", "Events/Activities removed.")
        else:
            show_message("Aborted", "Removal canceled.")
        

def search_list(ev: Global, events: Variable, text: str, dates: Global):
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
    events.set(events2)
    dates.set(dates2)
    

def writedownevent(name: ttk.Entry, time1: ttk.Spinbox, time2: ttk.Spinbox, calendar: Calendar, eventsV: Variable, dates: Global, ev: Global):
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
        eventsV.set(events2)
        dates.set(dates2)
    else:
        day: Day = read_back(date) #type: ignore
        events: dict = day.events
        if n in events.keys():
            if ask("Warning", "Writing down an activity/event with the same name\n\
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
                eventsV.set(events2)
                dates.set(dates2)
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
            eventsV.set(events2)
            dates.set(dates2)
    if not aborted:
        show_message("Done", "Information recorded!")
    else:
        show_message("Aborted", "Information discarded.")
    
def show_message(title, text):
    msg = ttk.Toplevel(title=title)
    ttk.Label(msg, text=text, font=tkFont.Font(family="Arial", size=12)).pack(padx=3, pady=3)
    msg.update()
    sleep(1)
    msg.destroy()

def ask(title, text):
    msg = ttk.Toplevel(title=title)
    frame = ttk.Frame(msg)
    ttk.Label(frame, text=text, font=tkFont.Font(family="Arial", size=12)).grid(row=0, column=0)
    ttk.Label(frame, image = "::tk::icons::warning").grid(row=0, column=1)
    frame.pack(padx=3, pady=3)
    frame2 = ttk.Frame(msg)
    yes = ttk.Button(frame2, bootstyle='success', command=lambda: yes.destroy(), text="Yes").grid(row=0, column=0, padx=5)
    no = ttk.Button(frame2, bootstyle='danger', command=lambda: no.destroy(), text="No").grid(row=0, column=1)
    frame2.pack(anchor='e', pady=3, padx=3)
    while(yes.winfo_exists() and no.winfo_exists() and msg.winfo_exists()):
        msg.update()
    
    if not msg.winfo_exists():
        return False
    
    if yes.winfo_exists():
        msg.destroy()
        return False
    else:
        msg.destroy()
        return True
    
