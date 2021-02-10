
    #########################################
    #   OPEN CV INSTALATION                 #
    #                                       #
    #   sudo apt update                     #
    #   sudo apt install python3-opencv     #
    #########################################


import numpy,cv2,socket,io,time                                         # only for variable size required
SocId = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)    # Socketidentification
SrvAdr = ("217.61.120.98", 20021)                                       # ServerAdress

cap = cv2.VideoCapture(0)       # 0 or 1 depending on whether you have 2 cameras (laptop)
cap.set(3, 320)                 # for laptop 1280x720, for camera 2048x1536
cap.set(4, 180)                 # low quality to ensure video stream 320x180
cap.set(cv2.CAP_PROP_FPS, 30)
cnt = 0                         # image counter
cntp = 0                        # counterpackages
#Part = bytearray(508)


while True:
    cnt += 1
    Ret, NpImg = cap.read()                             # ret unimportant, AIMG = ArrayImage
    #cv2.imwrite("Images/Img"+str(cnt) +".jpg", NpImg)
    #NpImg = cv2.resize(NpImg, (320, 180))              # downsize the image for stream
    
    #cv2.imshow('Stream', NpImg)                        # 1st argument = window name
    #cv2.waitKey(1)
    
    Ret, JAImg = cv2.imencode('.jpg', NpImg)            # JImg = JpgImage, ArrayImage coverting to JPGImage
    JImg = JAImg.tobytes()                              # Jpg_numpy_Image to jpg_Image
    stream = io.BytesIO(JImg)
    cntp = 0
    #print('size: ' + str(len(JImg)))
    while True: 
        
        part = stream.read(508-2)                       # 508-2 is the best
        cntp += 1
        if not part:
            #print('counter: ' + str(cntp))
            break
        part = (cntp).to_bytes(2, byteorder='big') + part    
        SocId.sendto(part, SrvAdr)
    stream.close()
    SocId.sendto(str.encode('End of Image'), SrvAdr)
    print(str(cnt)+' Image send')
    #time.sleep(0.01)
    
    