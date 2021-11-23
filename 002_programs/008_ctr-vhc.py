# dont delete this line, help us make the project known :)
print('open-source project by www.OPEN-ATS.eu \n change to your own IP and password')

import os, socket, threading, time

os.system('sudo pigpiod')	# starting GPIO deamon 
os.system('clear')			# not needed but otherwise a annoying message appears
time.sleep(1)				# it's too impatient and so if this delay is removed you will get an error
import pigpio				# importing GPIO library

pwd = b'rmxmjwby'	# password
kav = b'a vhc '  	# keepalive message, "a" stands for "alive", an indication

soc = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM) # internet protocol parameters
adrSrv = ('217.61.120.98', 3274)  # address server (ip and port)
soc.sendto(kav + pwd, adrSrv) # before something can be received, something must be sent! (otherwise an error appears)

tod = 0 # time of disconnect
PWM = pigpio.pi().set_servo_pulsewidth # just shorting that long name
cDa = [800, 800, 800, 800] # list with control data

def fkav(): # function to continuously sending keepalive data 
    while True:
        time.sleep(1) 	# sending every second
        soc.sendto(kav + pwd, adrSrv)
        print('sent:     keepalive and pwd')

def fsvd(): # function to stop vehicle when disconnected
    while True:
        global tod	# neccessary to write 'global' to WRITE a variable inside a thread
        time.sleep(0.05) # 50 ms
        tod += 1
        if tod >= 5: # after 250ms the vehicle stops
            # \033[91m equals color red; \033[0m  equals color white
            print('\033[91m vehicle for 0.25s disconnected: motor stopped \033[0m')
			# sending controll data to the output GPIO pins
            PWM( 18, 1500) # drive motor, right in drive direction														change to new PINS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            PWM( 23, 1500) # drive motor, left in drive direction
            
threading.Thread(target=fakv).start() # starting fkav as thread
threading.Thread(target=fsvd).start() # starting fsvd as thread

print('controlling vehicle running')
while True: # main loop, receiving controll data and outputting them on the GPIO pins
    msg, address = soc.recvfrom(1024)
    print('received: ' + msg.decode())
    tod = 0 # setting to 0 cause if data is received it's no longer disconnect
    if msg.decode()[0] == 'd': # just real data is accepted and no alive data
        cDa = msg.split() # split data and put in list
		# sending controll data to the output GPIO pins 
        PWM( 15, int(cDa[1])) # steering motor, right in drive direction									change to new PINS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        PWM( 18, int(cDa[2])) # steering motor, left in drive direction
        PWM( 23, int(cDa[3])) # drive motor, right in drive direction
        PWM( 24, int(cDa[3])) # drive motor, left in drive direction

# code maintained by Lukas Pfitscher (lukaspfitscher@open-ats.eu)