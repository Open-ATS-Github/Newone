
    #######################################
    #   change to your IP and password    #
    #######################################

import socket
pwd=b'rmxmjwby'#password
soc=socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM)#internet protocol parameters
soc.bind(('217.61.120.98',3274))    #address server (ip and port)
adrGrs  =('0.0.0.0',5000)           #address ground station
adrVhc  =('0.0.0.0',5000)           #address vehicle

print(' udp server up and listening ')
while True:
    msg,adr=soc.recvfrom(1024)#msg: message, adr: incoming address 
    print('received: '+msg.decode())
    
    if adr==adrGrs:
        soc.sendto(msg,adrVhc)#sent to vehicle
    elif adr==adrVhc:
        soc.sendto(msg,adrGrs)#sent to ground station
        
    elif msg==b'a grs '+pwd:
        adrGrs=adr#setting address for ground station
    elif msg==b'a vhc '+pwd:
        adrVhc=adr#setting address for vehicle