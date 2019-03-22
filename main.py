import serial

from tkinter import *
from tkinter import scrolledtext

window= Tk()
window.title("SELC - Practica 1")
window.geometry('500x400')

txt = scrolledtext.ScrolledText(window,width=40,height=10)
txt.grid(column=0,row=0)

lbl=Label (window, text="")
lbl.grid(column=0, row=1)

def clicked():
    txt.insert(INSERT,'Success')
    txt.insert(INSERT,'\n')
    txt.insert(INSERT,'Success1')

btn=Button(window, text="A", command=clicked)
btn.grid(column=1, row=0)

btn=Button(window, text="B", command=clicked)
btn.grid(column=2, row=0)

btn=Button(window, text="5", command=clicked)
btn.grid(column=3, row=0)

window.mainloop()
