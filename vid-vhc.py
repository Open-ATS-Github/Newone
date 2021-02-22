
    #######################################
    #   open CV installation              #
    #                                     #
    #   sudo apt update                   #
    #   sudo apt install python3-opencv   #
    #                                     #
    #   change to your IP and password    #
    #######################################

import numpy,cv2,socket,io,time 
pwd=b'rmxmjwby'#password
soc=socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM)#internet protocol parameters
adrSrv=('217.61.120.98',4582)#addresse server (ip and port)

cap=cv2.VideoCapture(0) #0 or 1, depending on whether you have 2 cameras (laptop)
cap.set(3,320)          #3 argument: with, for laptop 1280x720, for camera 2048x1536
cap.set(4,180)          #4 argument: high, low quality to ensure video continuous stream 320x180
cap.set(5,30)           #5 argument: FPS
cnt=0                   #image counter

while True:
    cnt+=1
    _,npImg=cap.read()#_ means first variable not needed, npImg = numpy array image
    
    #uncomment this lins to save the images
    #cv2.imwrite("Images/Img"+str(cnt)+".jpg",npImg)
    #npImg=cv2.resize(npImg,(320,180))#downsize the image for stream
    
    #uncomment this if you want to show the image
    #cv2.imshow('Stream',npImg)#1st argument = window name
    #cv2.waitKey(1)
    
    #_ means first variable not needed, ArrayImage coverting to JPGImage
    _,jImg=cv2.imencode('.jpg',npImg)#jImg: JpgImage
    stream=io.BytesIO(jImg)
    while True: 
        part=stream.read(506)#ref: https://stackoverflow.com/a/35697810
        if not part:break    
        soc.sendto(part,adrSrv)
    stream.close()
    soc.sendto(b'a vhc '+pwd,adrSrv)#indincation
    print('image sent '+str(cnt))