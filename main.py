import serial

from tkinter import *
from tkinter import scrolledtext

global unlockScreen2
unlockScreen2 = False

def serial_connection():
    COMPORT = 3
    global ser
    ser = serial.Serial()
    ser.baudrate = 38400
    ser.port = "COM"+ str(COMPORT - 1) #counter for port name starts at 0
    ser.flushInput()

    #check to see if port is open or closed
    if (ser.isOpen() == False):
        print ('The Port %d is Open '%COMPORT + ser.portstr)
          #timeout in seconds
        ser.timeout = 10
        ser.open()
    else:
        print ('The Port %d is closed' %COMPORT)

##serial_connection() ##Uncomment for opening the serial connection

window= Tk()
window.title("SELC - Practica 1")
##window.geometry('500x400')

txt = scrolledtext.ScrolledText(window,width=40,height=10)
txt.grid(column=0,row=0)

def onClick1():
    ser.write('A')
    txt.insert(INSERT,'A sent\n')

def onClick2():
    global ser
    ser.write('B')
    txt.insert(INSERT,'B sent\n')

def onClick3():
    ser.write('5')
    txt.insert(INSERT,'5 sent\n')

def onClick4():
    while True:
        try:
            ser_bytes = ser.readline()
            decoded_bytes = float(ser_bytes[0:len(ser_bytes)-2].decode("ascii"))
            txt.insert(INSERT,'You sent:' + str(decoded_bytes)+'\n')

            #Check conditions for unlock the 2nd screen

            # if (checkCondition):
            #     ##Unlock Screen 2 button
            #     global unlockScreen2
            #     unlockScreen2=True
            # else:
            #     txt.insert(INSERT,'Wrong code, try again.')
            break
        except:
            print("error")
            break

def onClick5():
    if (unlockScreen2==True):
        window2= Tk()
        window2.title("SELC - Hito 2")
        window2.geometry('500x400')

btn=Button(window, text="A", command=onClick1)
btn.grid(column=2, row=0, padx= 15)

btn=Button(window, text="B", command=onClick2)
btn.grid(column=3, row=0, padx= 15)

btn=Button(window, text="5", command=onClick3)
btn.grid(column=4, row=0, padx= 15)

btn=Button(window, text="Read data", command=onClick4)
btn.grid(column=5, row=0, padx= 15)

btn=Button(window, text="Next Stage", command=onClick5)
btn.grid(column=0, row=1, pady= 20)

window.mainloop()

ser.close()
