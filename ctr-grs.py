
    #######################################
    #       Pygame Instalation            #
    #       pip install pygame            #
    #                                     #
    #   change to your IP and password    #
    #######################################

import threading,socket,time,os,pygame
os.system('mode con: cols=50 lines=45')#window shape
pwd=b'rmxmjwby' #password
kav=b'a grs '   #keepalive message, "a" stands for "alive", an indication

soc=socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM)#internet protocol parameters
adrSrv=('217.61.120.98',3274)#address server (ip and port)
#must be done otherwise an error appears (before receiving something, something has to be sent!)
soc.sendto(kav+pwd,adrSrv)

sFR=1500    #servomotor front right 
sFL=1500    #servomotor front left
mtr=700     #motor 
ctd=''      #control data
cDO=''      #control data old

pygame.init()#needed for joystick
while pygame.joystick.get_count()==0:#checking if a joystick is connected
    print('joystick not connected, press enter to exit')
    input(); exit(1)#waiting for enter and exiting program
jys=pygame.joystick.Joystick(0)#create a joystick object
jys.init()
print('detected joystick:     ',jys.get_name())#name of the joystick

def t1():#thread for reciving data 
    while True:
        msg,adr=soc.recvfrom(1024)#msgb: message; adr: address
        print('received: '+msg.decode())

def t2():#thread for sending a keepalive package every second
    while True:
        soc.sendto(kav+pwd,adrSrv)
        print('sent:    keepalive and PWD')
        time.sleep(1)#sending an keepalive every second
       
threading.Thread(target=t1).start()#thread for receiving controll data
threading.Thread(target=t2).start()#thread for sending a keepalive package every second

print('steering:   LT,RL')#initial information
print('accelerate: left stick','\n')
print(' groud station is up and runing ')
   
while True:#main loop, reading controller input and sending it to the server 
    time.sleep(0.01)#loop is to fast to send continously (to much data)
    for event in pygame.event.get():
        if event.type==pygame.JOYAXISMOTION:
            #the controller gives a number between -1&1 and 
            #you need to convert it to number between 0-2500 for the servos
            sFR=int(round((+jys.get_axis(2)+1)/2*400+1250))#1450 is the mittle    
            sFL=int(round((+jys.get_axis(2)+1)/2*400+1450))#1650 is the mittle        
            if int(round((-jys.get_axis(1)+1)/2*1000+1000))<1300:mtr=1300#breaking just goes down to 1300                
            else:mtr=int(round((jys.get_axis(1)+1)/2*1000+1000))       

        ctd=('d '+str(sFR)+' '+str(sFL)+' '+str(mtr))#d stands for data, an indication for data category               
        if ctd!=cDO:#only sending if controll data changes
            soc.sendto(ctd.encode(),adrSrv)
            print('sent:    '+'FR:'+str(sFR)+' FL:'+str(sFL)+' motor:'+str(mtr))
        cDO=ctd