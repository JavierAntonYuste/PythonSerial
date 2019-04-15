import tkinter as tk
import serial as serial
from tkinter import *
from tkinter import scrolledtext
from tkinter import simpledialog

import mysql.connector as mysql

import threading
import time


baudrate = 115200
stop_threads=False


##Connection with serial property

def serial_connection():

    global ser
    ser = serial.Serial('/dev/ttyUSB0', baudrate= baudrate)  # open serial port
    print(ser.name)         # check which port was really used
    # ser.write(b'hello')     # write a string
    ser.close()

    #check to see if port is open or closed
    if (ser.isOpen() == False):
        print ('The Port %s is Open '% ser.portstr)
          #timeout in seconds
        ser.timeout = 10
        ser.open()
    else:
        print ('The Port is closed')

serial_connection() ##Uncomment for opening the serial connection

##Connection with DDBB
db = mysql.connect(
    host= "localhost",
    user= "javi-anton",
    passwd = "",
    database = "pie2018"
)

cursor =db.cursor()

class Object(tk.Tk, object):
    def __init__(self):
        super(Object, self).__init__()
        global master
        master = tk.Canvas(self, width=500, height=450)
        master.pack()

        self.btn1=Button(master, text="Empezar intento", command=lambda: self.onClickStart(self.btn1), bd=3, bg = "ForestGreen")
        self.btn1.place(x=175, y=200)

    def onClickStart(self, event):
        self.btn1.place_forget()

        self.scroll=scrolledtext.ScrolledText(master, width=50,height=20)
        self.scroll.place(x=40,y=25)

        self.btn2=Button(master, text="Terminar intento", command=lambda: self.onClickStop(self.btn2), bd=3, bg = "IndianRed")
        self.btn2.place(x=175, y=385)

        global startingTry
        startingTry = time.time()
        self.startTry()

    def onClickStop(self, event):
        global stop_threads
        stop_threads=True

        global startingTry
        stopingTry = time.time()
        duration= stopingTry-startingTry

        self.scroll.insert(INSERT, '\nHa acabado satisfactoriamente el intento.\n')
        self.scroll.insert(INSERT, 'Duracion del intento: ' + str(round(duration,3)) + '\n')
        self.scroll.see("end")

        self.btn2.place_forget()


    def startTry(self):
        t1 = threading.Thread(target=self.read, args=())
        t1.start()

    def read(self):
        time_start = 0
        time_stop = 0
        global stop_threads
        while True:
            rawData= ser.readline()

            if stop_threads:
                break

            data = rawData.replace(" ","").strip().split(",")

            self.scroll.insert(INSERT, '\nPuesto ' + str(data[0])+ '\n')
            self.scroll.insert(INSERT,  'Pulsacion ' + str(data[1])+ '\n')

            action = int(data[2])

            if (action==1):
                #Esperar hasta que apague el boton
                self.scroll.insert(INSERT, 'Ha pulsado el boton\n')
                self.scroll.insert(INSERT, 'Deje de pulsar el boton cuando acabe el disparo.\n')
                self.scroll.see("end")
                time_start =time.time()

            elif(action==0):
                if time_start==0:
                    continue
                time_stop=time.time()
                diff= time_stop - time_start
                self.scroll.insert(INSERT, 'Ha soltado el boton\n')
                self.scroll.insert(INSERT, 'Duracion de la pulsacion: ' + str(round(diff,3)) + '\n')
                self.scroll.see("end")
                #Escribir tiempo en base de datos
                registerTime(data, diff)


def registerTime (data, duration):
    user_id = data[0].strip('P')
    try:
        query = "INSERT INTO shoots (user_id, pulse_id, duration) VALUES" + "(" +  str(user_id)+ "," + str(data[1])+ "," + str(round(duration,3))+")"
        cursor.execute(query)
        db.commit()
    except:
        print("Error: Not able to update points")



if __name__ == "__main__":
    Object().mainloop()
