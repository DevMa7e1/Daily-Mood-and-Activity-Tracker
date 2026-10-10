import ttkbootstrap as ttk
import tkinter.font as tkFont
import calendar, datetime
import random
import windows

root = ttk.App(title='DM&AT')
root.theme_use('bootstrap-dark')
introduction = ttk.Frame(root)
introduction.grid(row=0, column=0, pady=(0, 10), padx=0)
ttk.Label(introduction, text='Hello!', font=tkFont.Font(family="Arial", size=25), justify='left', anchor="w").pack(anchor='w')
ttk.Label(introduction, text='Would you like to...').pack(anchor='w')

daycount = calendar.monthrange(datetime.datetime.now().year, datetime.datetime.now().month)[1]
display = ttk.Frame(root)
display.grid(row=2, column=1)
for x in range(4):
    for y in range(7):
        color = random.randint(0, 2)
        if color == 0:
            ttk.Button(display, text="X", bootstyle="primary").grid(row=x, column=y)
        elif color == 1:
            ttk.Button(display, text="X", bootstyle="success").grid(row=x, column=y)
        elif color == 2:
            ttk.Button(display, text="X", bootstyle="danger").grid(row=x, column=y)
for y in range(daycount-28):
    ttk.Button(display, text="X", bootstyle="success").grid(row=4, column=y)
for y in range(7-daycount+28):
    ttk.Button(display, text="X", bootstyle="secondary outline", state='disabled').grid(row=4, column=daycount-28+y)
menu = ttk.Frame(root)
menu.grid(row=2, column=0)
ttk.Button(menu, text="Add today's mood", bootstyle='info outline', command=windows.addmood).pack(anchor="w", padx=(2, 10), pady=3)
ttk.Button(menu, text="Add an activity", bootstyle='info outline').pack(anchor="w", padx=(2, 10), pady=3,)
ttk.Button(menu, text="Search activities", bootstyle='info outline').pack(anchor="w", padx=(2, 10), pady=3)
ttk.Button(menu, text="View all months", bootstyle='info outline').pack(anchor="w", padx=(2, 10), pady=3)

root.resizable(width=False, height=False)
root.mainloop()