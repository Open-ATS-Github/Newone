
    #####################################
    #   Change to your IP and Port      #
    #####################################

import socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind(("217.61.120.98", 20005))
address0 = ("0.0.0.0", 5000)     
address1 = ("0.0.0.0", 5000)
address2 = ("0.0.0.0", 5000)

print("udp server up and listening")

while True:
    message, address0 = UDPServerSocket.recvfrom(1024)
    print ("Received: "+str(message.decode()))
    if address0 == address1 :
        UDPServerSocket.sendto(message, address2)
    elif address0 == address2 :
        UDPServerSocket.sendto(message, address1)
    else:
        address2 = address1
        address1 = address0 
        print(address1)
        print(address2)