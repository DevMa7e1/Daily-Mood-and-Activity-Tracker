import ttkbootstrap as ttk
import tkinter.font as tkFont
import datetime
from calendar import monthrange
from record import read_month_ratings
import windows
from record import initialize

root = ttk.App(title='DM&AT')
root.theme_use('bootstrap-dark')
introduction = ttk.Frame(root)
introduction.grid(row=0, column=0, pady=5, padx=10, sticky='w')
ttk.Label(introduction, text='Hello!', font=tkFont.Font(family="Arial", size=25), justify='left', anchor="w").pack(anchor='w')
ttk.Label(introduction, text='Would you like to...').pack(anchor='w')
initialize()

daycount = monthrange(datetime.datetime.now().year, datetime.datetime.now().month)[1]
display = ttk.Frame(root)
display.grid(row=2, column=1)
ratings = read_month_ratings(datetime.datetime.now())
todaysbutton = None
for x in range(4):
    for y in range(7):
        b = None
        if ratings[x*7+(y+1)] == 11:
            b = ttk.Button(display, text="X", bootstyle="secondary")
            b.grid(row=x, column=y)
        elif ratings[x*7+(y+1)] < 5:
            b = ttk.Button(display, text="X", bootstyle="danger")
            b.grid(row=x, column=y)
        elif ratings[x*7+(y+1)] == 5:
            b = ttk.Button(display, text="X", bootstyle="primary")
            b.grid(row=x, column=y)
        elif ratings[x*7+(y+1)] > 5:
            b = ttk.Button(display, text="X", bootstyle="success")
            b.grid(row=x, column=y)
        if datetime.datetime.now().day == x*7+(y+1):
            todaysbutton = b
            
for y in range(daycount-28):
    b = None
    if ratings[28+(y+1)] == 11:
        b = ttk.Button(display, text="X", bootstyle="secondary")
        b.grid(row=4, column=y)
    elif ratings[28+(y+1)] < 5:
        b = ttk.Button(display, text="X", bootstyle="danger")
        b.grid(row=4, column=y)
    elif ratings[28+(y+1)] == 5:
        b = ttk.Button(display, text="X", bootstyle="primary")
        b.grid(row=4, column=y)
    elif ratings[28+(y+1)] > 5:
        b = ttk.Button(display, text="X", bootstyle="success")
        b.grid(row=4, column=y)
    if datetime.datetime.now().day == 28+(y+1):
        todaysbutton = b
for y in range(7-daycount+28):
    ttk.Button(display, text="X", bootstyle="secondary outline", state='disabled').grid(row=4, column=daycount-28+y)
menu = ttk.Frame(root)
menu.grid(row=2, column=0)
ttk.Button(menu, text="Add today's mood", bootstyle='info outline', command=lambda: windows.addmood(todaysbutton)).pack(anchor="w", padx=(2, 10), pady=3)
ttk.Button(menu, text="Add/remove activities", bootstyle='info outline', command=windows.addactivity).pack(anchor="w", padx=(2, 10), pady=3,)
ttk.Button(menu, text="Search all activities", bootstyle='info outline').pack(anchor="w", padx=(2, 10), pady=3)
ttk.Button(menu, text="View all months", bootstyle='info outline').pack(anchor="w", padx=(2, 10), pady=3)

root.resizable(width=False, height=False)
root.mainloop()