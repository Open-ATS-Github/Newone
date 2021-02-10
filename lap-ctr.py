
    #####################################
    #                                   #
    #       Pygame Instalation          #
    #       pip install pygame          #
    #                                   #
    #   Change to your IP and Port      #
    #                                   #
    #####################################

import _thread
import socket
import keyboard
import time
from os import environ                          #to execute the environ['PYGAM... comand
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'     #otherwise an annoying pygame message comes up
import os
os.system('mode con: cols=50 lines=45')         #window shape

import pygame
pygame.init()

ClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
serverAddressPort   = ("217.61.120.98", 20005)
#must be done otherwise an error appears, before receiving something, something has to be send
ClientSocket.sendto(str.encode('A Alive from Laptop'), serverAddressPort) 

servoFR =  1500     # front right
servoFL =  1500     # front left
motor  =  700       # motor    
msgbfr  = ''        # message before
msg     = ''        # message
counter = 0
stp = 10

joysticks = []
clock = pygame.time.Clock()
for i in range(0, pygame.joystick.get_count()):                     # for al the connected joysticks
    joysticks.append(pygame.joystick.Joystick(i))                   # create a Joystick object in our list
    joysticks[-1].init()                                            # initialize them all (-1 means loop forever)
    print ("Detected joystick:     ",joysticks[-1].get_name())      # print a statement telling what the name of the controller is

def t1(thread1):

    global servoFR, servoFL, motor, datalist, stp, msgbfr, counter, clock
    while True: 
            
        clock.tick(60)
        for event in pygame.event.get():
            
            if event.type == pygame.JOYAXISMOTION:
                servoFR   = int(round((+joysticks[event.joy].get_axis(2)+1)/2*400+1250))    #1450  is the mittle    
                servoFL   = int(round((+joysticks[event.joy].get_axis(2)+1)/2*400+1450))    #1650  is the mittle        #right stick:   Rechts: 700     links: 2200 
                
                #motor     = int(round((-joysticks[event.joy].get_axis(1)+1)/2*1000+1500))
                if int(round((-joysticks[event.joy].get_axis(1)+1)/2*1000+1000)) < 1300:    #breaking just goes down to 1300                
                    motor = 1300
                else:
                    motor   = int(round((-joysticks[event.joy].get_axis(1)+1)/2*1000+1000))       

            msg =   ('D' + ' '                      #D means Data, just an indication
                    + str(1500) + ' '               
                    + str(1500) + ' ' 
                    + str(servoFR) + ' ' 
                    + str(servoFL) + ' ' 
                    + str(motor)  )
                
            if msg != msgbfr :                                                  # only sending if controll data changed 
                ClientSocket.sendto(str.encode(msg), serverAddressPort)         # (main loop is to fast to send continously.. to much data)
                print('Send:    ' + msg)
            msgbfr = msg   

def t2(thread2):        #thread for keep alive data every second, 
    while True:         #A stands for Alive, just an indication
        time.sleep(1)   #sending an "alive" every second
        ClientSocket.sendto(str.encode('A Alive from Laptop'), serverAddressPort)
        print('Send:    ' + 'A Alive from Laptop')
       
_thread.start_new_thread(t1,("Thread1",))
_thread.start_new_thread(t2,("Thread2",)) 
 
print ("Groudstation is up and runing")             #initial information
print ("Steering:               right stick")
print ("Accelerate:             left  stick")
print ("ESC 0,500,700,2500:     Button 1,2,3,4")
print ("")
print ("Controller up and running")


while True: #reciving data 
    massage, address = ClientSocket.recvfrom(1024)
    msg = str(massage.decode())
    print("Recived: " + msg)

    
    




