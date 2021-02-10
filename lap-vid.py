
    #####################################
    #   Change to your IP and Port      #
    #####################################

import socket,os,cv2,io
import numpy as np

SocId = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)    # socket identification
SrvAdr   = ("217.61.120.98", 20021)                                     # server address
SocId.sendto(str.encode('first message'), SrvAdr)
cntvp = 0 #counter lost pictures

while True:                                    
    BytAry = bytearray()                    # Byte array, here the image is saved                               
    while True: 
        Part, Adr = SocId.recvfrom(655350)  # wait for data to be received
        if Part == b'End of Image':         # if no more data comes
            print("image received")
            break  
        x = int.from_bytes(Part[0:2], 'big')            
        #print('Sequence: '+ str(x))
        Part = Part[2:]
        BytAry += Part
    np_img = np.asarray(BytAry)                                             # convert the input to an array
    try:
        AImg = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
        AImg = cv2.resize(AImg, (640, 360))
        #AImg = cv2.flip(AImg, 1)                                           # mirrors the image
        #AImg = cv2.line(AImg, ( 50,180) , (590,180) , (255,255,255),1)     # x,y
        #AImg = cv2.line(AImg, (320, 50) , (320,310) , (255,255,255),1)     # x,y
        #AImg = cv2.putText(AImg, 'Speed', (20, 40), cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2,cv2.LINE_AA)
        #AImg = cv2.line(AImg, (78, 35) , (140,35) , (0, 255,0),11)         # x,y
        cv2.imshow('Stream', AImg)
        cv2.waitKey(1)
        print(str(cntvp))
    except:
        print("display image failed!")
        cntvp += 1
        pass
    
