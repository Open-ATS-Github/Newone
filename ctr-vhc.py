
    #######################################
    #   change to your IP and password    #
    #######################################

import socket               #needed for sending data to the server
import threading            #needed for having parallel programs
import os                   #importing os library so as to communicate with the system
import time                 #importing time library to make Rpi wait because its too impatient   
os.system('sudo pigpiod')   #launching GPIO library
os.system('clear')          #not needed but otherwise a annoying message appears
time.sleep(1)               #it is too impatient and so if this delay is removed you will get an error
import pigpio               #importing GPIO library

pwd=b'rmxmjwby'             #password
kav=b'a vhc '               #keepalive message, "a" stands for "alive", an indication

soc=socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM)#internet protocol parameters
adrSrv=('217.61.120.98',3274)#address server (ip and port)
#must be done otherwise an error appears, before receiving something, something has to be sent!
soc.sendto(kav+pwd,adrSrv) 

#GPIO pins, right and left, if you look in drive direction
sFR=3                       #servomotor front right  
sFL=26                      #servomotor front left
mBR=2                       #motor back right
mBL=16                      #motor back left
tod=0                       #time of disconnect
pOt=pigpio.pi()             #pi output
cDa=[800,800,800,800,800]   #list with control data

def t1():
    while True:#keepalive connection to the server
        time.sleep(1)#sending every second
        soc.sendto(kav+pwd,adrSrv)
        print('sent:     keepalive and pwd')

def t2():
    global tod
    while True:
        time.sleep(1)
        tod+=1
        if tod>4:
            #\033[91m equals color red; \033[0m  equals color white
            print('\033[91m'+'vehicle for 5s disconnected: motor stopped'+'\033[0m')
            pOt.set_servo_pulsewidth(mBR,500)#switch off the right engine
            pOt.set_servo_pulsewidth(mBL,500)#switch off the left engine
            
threading.Thread(target=t1).start()
threading.Thread(target=t2).start()

print(' vehicle up and running ')
while True:
    msg,address=soc.recvfrom(1024)
    print('reciverd: '+msg.decode())
    tod=0#setting to zero cause if data is recived it's no longer disconnect
    if msg.decode()[0]=='d':#so just real data is accepted and no alive data
        cDa = msg.split()#data will split and added to list
        pOt.set_servo_pulsewidth(sFR,int(cDa[1]))#sending control data to servomotors front right
        pOt.set_servo_pulsewidth(sFL,int(cDa[2]))#sending control data to servomotors front left
        pOt.set_servo_pulsewidth(mBR,int(cDa[3]))#sending control data to motor back right
        pOt.set_servo_pulsewidth(mBL,int(cDa[3]))#sending control data to motor back left