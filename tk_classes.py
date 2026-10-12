import ttkbootstrap as ttk
from datetime import datetime
import tkinter.font as tkFont
from time import sleep
from record import modify, read_back
from classes import Global

class Event:
    def __init__(self, parent, name: str, date: datetime, command: (...), number: int):
        self.command = command
        element = ttk.Frame(parent, relief='raised', borderwidth=1)
        element.grid_rowconfigure(0, weight=1)
        element.grid_columnconfigure(0, weight=2)
        element.grid_columnconfigure(0, weight=1)
        labels = ttk.Frame(element)
        ttk.Label(labels, text=name, justify='left', borderwidth=0, font=tkFont.Font(family="Arial", size=12, weight='bold')).pack(pady=0, ipady=0, expand=True, fill='x')
        if date.timestamp() != 0:
            ttk.Label(labels, text=str(date), justify='left', font=tkFont.Font(family="Arial", size=8), borderwidth=0).pack(pady=0, ipady=0, expand=True, fill='x')
        labels.grid(column=0, row=0, sticky='ew', padx = 4)
        if date.timestamp() != 0:
            ttk.Button(element, bootstyle='danger', text="Delete", command = lambda: command()).grid(column=1, row=0, sticky='e', padx = 4, pady=4)
        else:
            ttk.Button(element, bootstyle='danger', text="Delete", command = lambda: command(), state='disabled').grid(column=1, row=0, sticky='e', padx = 4, pady=4)
        element.grid(padx = 4, pady = (4, 0), row=number, column=0, sticky='ew')
        self.destroy = lambda: element.destroy()

class EventList:
    def __init__(self, parent, events: list[str], dates: list[datetime], all_events: Global):
        self.events = events
        self.dates = dates
        self.frame = ttk.Frame(parent)
        self.frame.grid_columnconfigure(0, weight=1)
        self.ev = all_events
        number = 0
        self._evs = []
        for i in range(len(events)):
            self._evs.append(Event(self.frame, events[i], dates[i], lambda: self.delete(i), number))
            number += 1
    def update(self):
        number = 0
        newevs = []
        for jj in range(len(self.dates)):
            newevs.append(Event(self.frame, self.events[jj], self.dates[jj], lambda: self.delete(jj), number))
            number += 1
        if len(newevs) == 0:
            newevs.append(Event(self.frame, 'No activities', datetime.fromtimestamp(0), lambda a: (), 0))
        for i in self._evs:
            i.destroy()
        self._evs = newevs
    def delete(self, index: int):
        if MessageBox().ask("Wait", "Proceed with removing event/activity?"):
            day: Day = read_back(self.dates[index]) #type: ignore
            day.events.pop(self.events[index])
            modify(day)
            self.ev.value.remove((self.dates[index], self.events[index]))
            self.events.pop(index)
            self.dates.pop(index)
            self.update()
            MessageBox().show_message("Done", "Event/activity deleted.")
        else:
            MessageBox().show_message("Aborted", "Deletion canceled.")

class MessageBox:
    def show_message(self, title, text):
        msg = ttk.Toplevel(title=title)
        ttk.Label(msg, text=text, font=tkFont.Font(family="Arial", size=12)).pack(padx=3, pady=3)
        msg.update()
        sleep(1)
        msg.destroy()

    def ask(self, title, text):
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
            
        