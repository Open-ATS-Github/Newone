
    #####################################
    #   change to your IP and password  #
    #####################################

import socket
pwd=b'rmxmjwby'#password
soc=socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM)#internet protocol parameters
soc.bind(('217.61.120.98',4582)) #address server (ip and port)
adrGrs  =('0.0.0.0',5000)        #address ground station 
adrVhc  =('0.0.0.0',5000)        #address vehicle 

print(' udp server up and listening ')
while True:
    msg,adr=soc.recvfrom(1024)#reciving message, adr: incoming address
    if adr==adrGrs:
        soc.sendto(msg,adrVhc)#sent to vehicle
    #elif adr==adrVhc:#not needed for now
        #soc.sendto(msg,adrGrs)#sent to ground station 
    else:   
        try:
            if msg==b'a grs '+pwd:
                adrGrs=adr#setting address for ground station
                print('new login: adrGrs: '+str(adrGrs))
            elif msg==b'a vhc '+pwd:
                adrVhc=adr#setting address for vehicle
                print('new login: adrVhc: '+str(adrVhc))
        except:pass