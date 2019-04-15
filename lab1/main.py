import tkinter as tk
import serial as serial
from tkinter import *
from tkinter import scrolledtext
from tkinter import simpledialog

import threading
import time


i=0
baudrate = 115200

def serial_connection():

    global ser
    ser = serial.Serial('/dev/ttyUSB0', baudrate= baudrate)  # open serial port
    print(ser.name)         # check which port was really used
    # ser.write(b'hello')     # write a string
    # ser.close()

    #check to see if port is open or closed
    if (ser.isOpen() == False):
        print ('The Port %s is Open '% ser.portstr)
          #timeout in seconds
        ser.timeout = 10
        ser.open()
    else:
        print ('The Port is closed')

serial_connection() ##Uncomment for opening the serial connection



## Stage 1 __________________________________________________________________________________________
class Object(tk.Tk, object):
    def __init__(self):
        super(Object, self).__init__()
        global master
        master = tk.Canvas(self)
        #master.title("SELC - Practica 1")
        master.pack()

        ## FIRST SCREEN__________________________________________________________
        ##Placed Objects
        self.check1= tk.Button(master, text="Check",command=lambda: self.checkResult1(self.check1))
        self.check1.place(x=140, y=175)

        self.entry1 = Entry(master)
        self.entry1.place(x=95, y= 75)

        self.resultmess1 = Message(master, width = 150)
        self.resultmess1.place (x=130,y=125)

        self.mess1=Message(master, text= 'Introduza la tasa de decodificacion:', width = 300)
        self.mess1.place(x=60,y=25)

        self.btn11=Button(master, text="A", command=lambda: self.onClick1(self.btn11))
        self.btn11.place(x=85, y=225)

        self.btn12=Button(master, text="B", command=lambda: self.onClick2(self.btn12))
        self.btn12.place(x=160, y=225)

        self.btn13=Button(master, text="5", command=lambda: self.onClick3(self.btn13))
        self.btn13.place(x=235, y=225)

        #Built Objects
        self.btn1 = tk.Button(master, text='Siguiente pantalla', command=lambda: self.nextStage1(self.btn1))

    def checkResult1(self, event):
        result= self.entry1.get()
        if (result == str(baudrate)):
            self.btn1.place(x=105, y=175)
            self.check1.place_forget()
            self.resultmess1.config(text="CORRECTO", bg = "green", foreground = "white")
            self.entry1.config(state='disabled')
        else:
            self.resultmess1.config(text="INCORRECTO", bg ="red", foreground = "white")


    def nextStage1 (self, event):
        self.mess1.place_forget()
        self.entry1.place_forget()
        self.btn1.place_forget()
        self.btn11.place_forget()
        self.btn12.place_forget()
        self.btn13.place_forget()
        self.resultmess1.place_forget()
        self.buildStage2()


    def onClick1(self, event):
        ser.write('A')


    def onClick2(self, event):
        ser.write('B')

    def onClick3(self, event):
        ser.write('5')


## Stage 2 ____________________________________________________________________________________________

    def onClick4(self, event):
        ser.write('A')
        self.txt1.insert(INSERT,'A sent\n')

    def onClick5(self, event):
        ser.write('B')
        self.txt1.insert(INSERT,'B sent\n')

    def onClick6(self, event):
        ser.write('5')
        self.txt1.insert(INSERT,'5 sent\n')

    def read(self):
        i=0
        while True:
            i = i+1
            result=0

            while True:
                ser.read()
                size = ser.inWaiting()
                if size==0:
                    break

            data=ser.read()

            print "Data: " + data
            print("waiting " + str(ser.inWaiting()))

            try:
                #self.txt1.insert(INSERT,"Data received: " + str()) + " \n"
                if (data=='S'): ##Codigo del caracter deseado
                    break
            except:
                print ("No received data")

            time.sleep(0.1)

        self.nextStage2()

    def buildStage2(self):
        ##Elements in Screen 1
        global master

        self.txt1 = scrolledtext.ScrolledText(master,width=40,height=10)
        self.txt1.place(x=25, y=5)

        self.btn21=Button(master, text="A", command=lambda: self.onClick4(self.btn21))
        self.btn21.place(x=100, y=200)

        self.btn22=Button(master, text="B", command=lambda: self.onClick5(self.btn22))
        self.btn22.place(x=175, y=200)

        self.btn23=Button(master, text="5", command=lambda: self.onClick6(self.btn23))
        self.btn23.place(x=250, y=200)

        self.btn24 = tk.Button(master, text='Siguiente pantalla', command=lambda: self.buildStage3(self.btn21))
        self.resultmess2 = Message(master, width = 150)

        t1 = threading.Thread(target=self.read, args=())
        t1.start()

    def nextStage2(self):
        self.txt1.place_forget()
        self.btn21.place_forget()
        self.btn22.place_forget()
        self.btn23.place_forget()

        self.btn24.place(x= 100, y= 150)
        self.resultmess2.place(x=130, y=100)
        self.resultmess2.config(text="CORRECTO", bg = "green", foreground = "white")

##Stage 3_____________________________________________________________________
    def buildStage3(self,event):
        self.btn24.place_forget()
        self.resultmess2.place_forget()

        global master

        self.txt2 = scrolledtext.ScrolledText(master,width=40,height=10)
        self.txt2.place(x=25, y=5)

        self.btn31=Button(master, text="SELC", command=lambda: self.onClick7(self.btn31))
        self.btn31.place(x=100, y=200)

        self.btn32=Button(master, text="HOLA", command=lambda: self.onClick8(self.btn32))
        self.btn32.place(x=175, y=200)

        self.btn33=Button(master, text="BIEN", command=lambda: self.onClick9(self.btn33))
        self.btn33.place(x=250, y=200)

        t1 = threading.Thread(target=self.readWord, args=())
        t1.start()

    def onClick7(self, event):
        ser.write('SELC\n')
        self.txt2.insert(INSERT,'SELC sent\n')

    def onClick8(self, event):
        ser.write('HOLA\n')
        self.txt2.insert(INSERT,'HOLA sent\n')

    def onClick9(self, event):
        ser.write('BIEN\n')
        self.txt2.insert(INSERT,'BIEN sent\n')

    def readWord(self):
        i=0
        size=0
        result=[]

        while True:
            i = i+1
            result=0

            size = ser.inWaiting()
            data=ser.readline()
            # result.insert()

            data=data.strip()

            print "Data: " + data
            print("waiting " + str(ser.inWaiting()))

            try:
                #self.txt1.insert(INSERT,"Data received: " + str()) + " \n"


                if (data=='SELC'): ##Codigo del caracter deseado
                    break
            except:
                print ("No received data")

            time.sleep(0.1)

        finishStage(self)


def finishStage(self):
    self.txt2.place_forget()
    self.btn31.place_forget()
    self.btn32.place_forget()
    self.btn33.place_forget()

    self.resultmess3 = Message(master, width = 300)
    self.resultmess3.place(x=75, y=110)
    self.resultmess3.config(text="Has completado todo el laboratorio", bg = "green", foreground = "white")


if __name__ == "__main__":
    Object().mainloop()
