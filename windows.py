import ttkbootstrap as ttk
from tkinter import HORIZONTAL, END
import tkinter.font as tkFont
from time import sleep
from record import write_down, read_back, modify
from datetime import datetime
from classes import Day

def addmood():
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
    command=lambda val: label.config(text=str(round(float(val)))+'/10'))
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

    ttk.Button(window, text='Write down', bootstyle='danger outline', command=lambda: writedownmood(rating, word, window)).pack(anchor='e', padx=5, pady=5)

def addmoodhelp():
    msg = ttk.Toplevel(title="Help")
    ttk.Label(msg, text="Rating guide:", font=tkFont.Font(family="Arial", size=13)).pack(anchor='w')
    ttk.Label(msg, text="0 means extremely negative\n5 means neutral\n10 means extremely positive").pack()

def writedownmood(rating: ttk.Scale, word: ttk.Entry, window: ttk.Toplevel):
    if read_back(datetime.now()) == False:
        day = Day(datetime.now(), round(float(rating.get())), word=word.get())
        write_down(day)
    else:
        day: Day = read_back(datetime.now()) #type: ignore
        day.rating = round(float(rating.get()))
        day.word = word.get()
        modify(day)
    window.destroy()
    show_message('Done', 'Information recorded!')


def show_message(title, text):
    msg = ttk.Toplevel(title=title)
    ttk.Label(msg, text=text, font=tkFont.Font(family="Arial", size=12)).pack(padx=3, pady=3)
    msg.update()
    sleep(1)
    msg.destroy()
