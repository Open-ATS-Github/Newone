
    #####################################
    #   change to your IP and password  #
    #####################################

import socket,os,cv2,io,numpy
pwd=b'rmxmjwby'#password
soc=socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM)#internet protocol parameters
adrSrv=('217.61.120.98',4582)#address server (IP and port)

while True:
    #must be done otherwise an error appears (before receiving something, something has to be sent!)
    soc.sendto(b'a grs '+pwd,adrSrv)                                
    bytAry=bytearray()#byte array, here the image is saved                               
    while True:#loop where the individual packages are put together to form the picture
        part,adrSrv=soc.recvfrom(655350)#wait for data to be received
        #transmiting a random string has two usecases:
        #its an idication that the image ended
        if part==b'a vhc '+pwd:#if no more data comes
            print('image received')
            break#breaks the loop and displays the picture 
        bytAry+=part
    np_img = numpy.asarray(bytAry)#convert the input to an array
    try:
        aImg=cv2.imdecode(np_img,cv2.IMREAD_COLOR)
        #aImg=cv2.resize(aImg,(640,320))#uncomment for scaling the image
        #aImg = cv2.flip(aImg,1)#uncomment this for mirrors the image
        cv2.imshow('videostream',aImg)#first arg is the name of the window
        cv2.waitKey(1)
    except:pass