import tkinter as tk
import serial as serial
from tkinter import *
from tkinter import simpledialog

import mysql.connector as mysql

import threading
import time

baudrate = 115200
stop_threads=False
timeBeginLab=0
timeTotal=0
counting = False
userName=""

# Connection with serial property
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

        # root = tk.Tk()
        # width = root.winfo_screenwidth()
        # height = root.winfo_screenheight()
        # root.geometry("%dx%d" % (width, height))


        global master, width, height
        width=self.winfo_screenwidth()
        height=self.winfo_screenheight()

        master = tk.Canvas(self, width=width, height=height,  highlightthickness=0)
        master.pack(fill = "both", expand = True)
        master.config(bg="black")
        master.pack()

        self.txt1 = Label( master, fg="white", font= "Helvetica 40", bg="black", width = 500)
        master.create_window(width/2, height/2, window=self.txt1)

        self.txt2 = Label ( master, fg="ForestGreen", font= "Helvetica 80 bold" , bg="black" , width = 500, text= "Empiece a disparar")
        master.create_window(width/2, (2*height)/5, window=self.txt2)
        self.txt3 = Label ( master, fg="white", font= "Helvetica 40", bg="black" , width = 500)
        master.create_window(width/2, (5*height)/2, window=self.txt3)

        self.btn1=Button(master, text="Terminar intento", command=lambda: self.onClickStop(self.btn1), bd=2, bg = "IndianRed")
        self.btn1.place(x=615, y=600)

        self.startTry()

    def startTry(self):
        t1 = threading.Thread(target=self.read, args=())
        t1.start()

    def onClickStop(self, event):
        ser.close()

        global timeTotal, data, userName, puntosPerdidos, stop_threads,timeTry, count, counting, time_start, time_stop, timeBeginLab
        registerTimeTotal(data, timeTotal)
        user_id = userName.strip('P')
        timeTries=0
        try:
            query= "SELECT duration FROM shoots WHERE user_id = " + str(user_id)
            cursor.execute(query)
            records = cursor.fetchall()

            if len(records)!=0:
                for trying in records:
                    timeTries= timeTries + trying[0]

        except:
            print("Not able to get points")

        puntosPerdidos= 50 * timeTotal + 10*timeTries

        print ("Puntos perdidos = " + str(puntosPerdidos))

        stop_threads=True
        timeTotal=0
        count = 0
        counting = False
        time_start=0
        time_stop=0
        timeBeginLab=0

        #time.sleep(5)
        ser.open()


        self.btn1.place_forget()

    def countUp(self, event):
        global count, counting
        if counting == True:
            count = count + 0.1
            self.txt2.configure(text=str(count) + " s")
            master.create_window(width/2, (2*height)/5, window=self.txt2)
            master.after(100, self.countUp, count+0.01)

    def read(self):
        global time_start, time_stop, timeBeginLab, data, stop_threads, userName,count, counting, timeTotal
        time_start = 0
        time_stop = 0
        while True:
            rawData= ser.readline()

            data = rawData.replace(" ","").strip().split(",")

            ##Cambio de Usuario
            if (data[0]!=userName or (int(data[2])==1 and timeBeginLab==0)):
                stop_threads=False
                self.btn1.place(x=615, y=600)

            userName = data[0]

            if stop_threads:
                continue

            self.txt1.configure(text="Tiempo Disparo " + str(data[1]))
            master.create_window(width/2, height/6, window=self.txt1)

            if time_start==0:
                self.txt3.configure(text="Total " + str(data[0]) + " : 0 segundos")
                master.create_window(width/2, (2*height)/3, window=self.txt3)

            action = int(data[2])

            if (action==1):
                if (data[0]!=userName or (int(data[2])==1 and timeBeginLab==0)):

                    timeBeginLab=time.time()
                time_start =time.time()

                count=0
                counting = True

                self.countUp(self)

            elif(action==0):
                counting = False
                if time_start==0:
                    continue
                time_stop=time.time()
                duration= time_stop - time_start

                timeTotal = time.time() - timeBeginLab

                self.txt3.configure(text="Total " + str(data[0]) + " : " + str(round(timeTotal,2))+ " segundos")
                master.create_window(width/2, (2*height)/3, window=self.txt3)

                #Escribir tiempo en base de datos
                registerTimeTry(data, duration)


def registerTimeTry (data, duration):
    user_id = data[0].strip('P')
    records = ""
    try:
        query = "SELECT user_id, pulse_id FROM shoots"
        cursor.execute(query)
        records = cursor.fetchall()

        if len(records)==0:
            query = "INSERT INTO shoots (user_id, pulse_id, duration) VALUES" + "(" +  str(user_id)+ "," + str(data[1])+ "," + str(round(duration,2))+")"
        else:
            for user in records:
                if (int(user_id)==user[0] and int(data[1])==user[1]):
                    query="UPDATE shoots SET duration= " + str(round(duration,2)) +" WHERE user_id=" + str(user_id) + " AND pulse_id=" + str(data[1])
                    break
                else:
                    query = "INSERT INTO shoots (user_id, pulse_id, duration) VALUES" + "(" +  str(user_id)+ "," + str(data[1])+ "," + str(round(duration,2))+")"

        cursor.execute(query)
        db.commit()
    except:
        print("Error: Not able to register timeTry")

def registerTimeTotal (data, duration):
    user_id = data[0].strip('P')
    try:
        query = "SELECT user_id FROM shootsTotal"
        cursor.execute(query)
        records = cursor.fetchall()

        if len(records)==0:
            query = "INSERT INTO shootsTotal (user_id, duration) VALUES" + "(" +  str(user_id)+ "," + str(round(duration,2))+")"
        else:
            for user in records:
                if (int(user_id)==user[0]):
                    query="UPDATE shootsTotal SET duration =" + str(round(duration,2)) + "WHERE user_id=" + str(user_id)
                    break
                else:
                    query = "INSERT INTO shootTotal (user_id, duration) VALUES" + "(" +  str(user_id)+ "," + str(round(duration,2))+")"

        cursor.execute(query)
        db.commit()
    except:
        print("Error: Not able to register timeTotal")


if __name__ == "__main__":
    Object().mainloop()
