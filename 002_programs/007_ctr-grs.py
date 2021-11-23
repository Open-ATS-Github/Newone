# dont delete this line, help us make the project known :)
print('open-source project by www.OPEN-ATS.eu \n change to your own IP and password')

import os, socket, threading, time
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" # annoying pygame support message
import pygame

pwd = b'rmxmjwby'	# password
kav = b'a grs '  	# keepalive message, "a" stands for "alive", an indication

soc = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM) # internet protocol parameters
adrSrv = ('217.61.120.98', 3274)  # address server (ip and port)
soc.sendto(kav + pwd, adrSrv) # before something can be received, something must be sent! (otherwise an error appears)

pygame.init()  # needed for joystick
if pygame.joystick.get_count() == 0:  # checking if a joystick is connected
    print('joystick not connected, program is terminated')
    exit() # exiting program
jys = pygame.joystick.Joystick(0)  # create a joystick object
jys.init()
print('detected joystick:     ', jys.get_name())  # name of the joystick

def fkav():  # function to continuously sending keepalive packages
    while True:
        soc.sendto(kav + pwd, adrSrv)
        print('sent:    keepalive and password')
        time.sleep(0.05) # 50 ms

print('controlling groud station running')
print('steering:   stick right')	# steerig information
print('accelerate: stick left \n')	# steerig information

threading.Thread(target = fkav).start() # starting funktion as thread
servoR = servoL = mtr = 800
while True:  # main loop to continuosly read control data and sending it
    time.sleep(0.01)  # sending controll data every 10 ms
    for event in pygame.event.get(): # 
        if event.type == pygame.JOYAXISMOTION:
			# change get_axis number for different steering with the gamepad
			# the controller gives a number between -1&1, converting to 0-2500
            servoR = int(round(jys.get_axis(3) * 300 + 1500))	# servomotor right
            servoL = int(round(jys.get_axis(3) * 300 + 1500))	# servomotor left
            mtr = int(round(jys.get_axis(1) * 50 + 1480)) 		# both drive motors
    soc.sendto(('d ' + str(servoR) + ' ' + str(servoL) + ' ' + str(mtr)).encode(), adrSrv)
    print('sent:    ' + 'FR:' + str(servoR) +' FL:' + str(servoL) + ' motor:' + str(mtr))

# code maintained by Lukas Pfitscher (lukaspfitscher@open-ats.eu)