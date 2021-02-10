
    #####################################
    #   change to your IP and Port      #
    #####################################

import os                   # importing os library so as to communicate with the system
import time                 # importing time library to make Rpi wait because its too impatient 
os.system ("sudo pigpiod")  # launching GPIO library
time.sleep(1)               # it is too impatient and so if this delay is removed you will get an error
import pigpio               # importing GPIO library
import _thread
import socket

servoHR =   2               # GPIO pin 
servoHL =   3               # right and left, if you look in drive direction
servoFR =   4               # front right  
servoFL =   17              # front left
motor   =   27

  

pi = pigpio.pi();

ClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
serverAddressPort   = ("217.61.120.98", 20005)
datalist  = [800,800,800,800,800]   #just some initial data
#must be done otherwise an error appears, before receiving something, something has to be send
ClientSocket.sendto(str.encode('first car to server connection'), serverAddressPort)           


tod = 0                 # time of disconnect

def t1(thread1):        # basically everything can written in the brackets
    while True:         # keeping the connection to the server alive
        time.sleep(1)
        ClientSocket.sendto(str.encode('A alive from car'), serverAddressPort)
        print('send:     ' + 'A alive from car')

def t2(thread2): 
    global tod
    while True:
        time.sleep(1)
        tod = tod + 1
        if tod > 4:
        
            print ('\033[91m' + "error:    car for 5s disconnected")    #\033[91m red
            print ("error:    initialising emergency protocol")
            print ("error:    motor set to 0")
            pi.set_servo_pulsewidth(motor,500)
            
print ("car up and running")
_thread.start_new_thread(t1,("Thread1",)) 
_thread.start_new_thread(t2,("Thread2",)) 

while True:
    msg, address = ClientSocket.recvfrom(1024)
    print ("reciverd: "+str(msg.decode()))
    tod = 0
    
    
    if str(msg.decode())[0] == 'D':         # so just real data is accepted and no alive data
    
        datalist = msg.split()
        pwmservoHR   = int(datalist[1])
        pwmservoHL   = int(datalist[2])
        pwmservoFR   = int(datalist[3])
        pwmservoFL   = int(datalist[4])
        pwmmotor    = int(datalist[5])
        
        pi.set_servo_pulsewidth(servoHR,pwmservoHR)
        pi.set_servo_pulsewidth(servoHL,pwmservoHL)
        pi.set_servo_pulsewidth(servoFR,pwmservoFR)
        pi.set_servo_pulsewidth(servoFL,pwmservoFL)
        pi.set_servo_pulsewidth(motor,pwmmotor)
        #if str(msg.decode()) == "right":
            #print ("plane turns right")
        #if str(msg.decode()) == "left":
            #print ("plane turns left")

    
    




