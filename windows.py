import ttkbootstrap as ttk
from tkinter import HORIZONTAL
import tkinter.font as tkFont

def addmood():
    window = ttk.Toplevel(title="What's today's mood?")
    ttk.Label(window, text="Rate this day on a scale from 0 to 10.", font=tkFont.Font(family="Arial", size=12)).pack()

    label = ttk.Label(window, text='5/10')
    rating = ttk.Scale(window, from_=0, to=10, orient=HORIZONTAL, length=100, value=5,\
    command=lambda val: label.config(text=str(round(float(val)))+'/10'))
    rating.pack(anchor='w')
    label.pack(anchor='w')

    ttk.Button(window, text='?', command=addmoodhelp, bootstyle='info outline').pack(anchor='e')

    ttk.Label(window, text="One word that describes today:", font=tkFont.Font(family="Arial", size=12)).pack(anchor='w')
    word = ttk.Entry(window)
    word.pack(anchor='w')
def addmoodhelp():
    msg = ttk.Toplevel(title="Help")
    ttk.Label(msg, text="Rating guide:", font=tkFont.Font(family="Arial", size=13)).pack(anchor='w')
    ttk.Label(msg, text="0 means extremely negative\n5 means neutral\n10 means extremely positive").pack()