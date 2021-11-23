# dont delete this line, help us make the project known :)
print('open-source project by www.OPEN-ATS.eu \n change to your own IP and password')

print('videostream gound station running')
print('waiting for images to be received')

import socket, os, cv2, io, numpy, time, threading
pwd = b'rmxmjwby'	# password
kav = b'a grs '		# keepalive message, "a" stands for "alive", an indication

soc = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM) # internet protocol parameters
adrSrv = ('217.61.120.98', 4582) # address server (IP and port)

def fkav(): # function to continuously sending keepalive messages
	while True:
		soc.sendto(kav+pwd, adrSrv)
		time.sleep(0.5) # 500 ms

threading.Thread(target = fkav).start() # starting funktion as thread
while True: # main loop, continously receiving video data and diplaying them
	# before something can be received, something must be sent! (otherwise an error appears)
	soc.sendto(kav+pwd, adrSrv) # sendig a alive package every time a picture is send
	bytAry = bytearray()  # byte array, where the image is saved
	while True:  # loop where the individual packages are put together to form the picture
		part, adrSrv = soc.recvfrom(655350)  # wait for data to be received
		if part == b'a vhc ' + pwd:  # if no more data comes, an indication that the image ended
			print('image received')
			break  # breaks the loop and displays the picture
		bytAry += part
	np_img = numpy.asarray(bytAry)  # convert the input to an array
	try:
		aImg = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
		#aImg = cv2.flip(aImg,1) # uncomment this for mirroring the image
		cv2.imshow('videostream', aImg)  # first arg is the name of the window
		cv2.waitKey(1)
	except:
		pass

# code maintained by Lukas Pfitscher (lukaspfitscher@open-ats.eu)