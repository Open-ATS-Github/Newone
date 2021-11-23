# dont delete this line, help us make the project known :)
print('open-source project by www.OPEN-ATS.eu \n change to your own IP and password')
     
import numpy, cv2, socket, io, time, threading
pwd = b'rmxmjwby'	# password
kav = b'a vhc '		# keepalive message, "a" stands for "alive", an indication

soc = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM) # internet protocol parameters
adrSrv = ('217.61.120.98', 4582)  # address server (ip and port)
soc.sendto(kav + pwd, adrSrv) # before something can be received, something must be sent! (otherwise an error appears)

cap = cv2.VideoCapture(0) # 0 or 1, depending on whether you have one or more cameras
# image size, 1280x720 or set to 320x180 to ensure lower quality continuous video stream
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280) # image width
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720) # image height
cap.set(cv2.CAP_PROP_FPS, 30)  			# FPS
cnt = 0  # image counter
tod = 0  # time of disconnect
print('videostream program running')

def frkm(): # function, receive keepalive messages
    global part, adrSrv, tod  # neccessary to write 'global' to WRITE a variable inside a thread
    while True:
        part, adrSrv = soc.recvfrom(655350)
        tod = 0  # time of disconnect

def fctd(): # function, count 'time of disconnect'
    global tod  # neccessary to write 'global' to WRITE a variable inside a thread
    while True:
        time.sleep(1)
        tod += 1
        if tod > 10: # after 10sec the videostream pauses to save trafic
            print('no connection to ground station, videostream paused')

threading.Thread(target = frkm).start() # starting funktion as thread
threading.Thread(target = fctd).start() # starting funktion as thread

while True: # main loop, for continuously taking and sending video data
    if tod < 5:
        cnt += 1
        npImg = cap.read()[1] # capturing image; tuple, only second element needed
        
        ## uncomment to save the images
        #cv2.imwrite("Images/Img"+str(cnt)+".jpg",npImg)
        #npImg=cv2.resize(npImg,(320,180)) # downsize the image for stream
        ## uncomment to show the image
        #cv2.imshow('Stream',npImg) # 1st argument = window name
        #cv2.waitKey(1)

        # numpy image to jpg; tuple (only second element needed)
        jImg = cv2.imencode('.jpg', npImg, [int(cv2.IMWRITE_JPEG_QUALITY), 90])[1] # tupsle
        stream = io.BytesIO(jImg) # creating a stream to continously taking chunks from the jpg file
        while True:
            part = stream.read(506) # 506 is the max UDP package lengh
            if not part: # if-block will execute if string is empty
                break
            soc.sendto(part, adrSrv)
        soc.sendto(kav + pwd, adrSrv) # multipurpose: authentication server, keepalive, indication end of image
        print('image sent ' + str(cnt))

# code maintained by Lukas Pfitscher (lukaspfitscher@open-ats.eu) & Spaltex