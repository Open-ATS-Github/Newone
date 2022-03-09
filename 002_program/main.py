#!/usr/bin/env python3

# short description of the individual subprograms:

# controlling groundstation: reads the input of the joystick and sends it to the vehicle through the server
# sending continuously keep alive sou the vehichle will stop when disconnected

# videostream groundstation: recives the image from the vehicle in junks, recombines it to a full image and displays it
# sendig alive messages so the vehicle wound send when the ground station isnt open to save trafic

# controlling vehicle: receiving control data from the ground station through the server and sets the outputs of the pi accordingly
# vehicle will stop if there is no connection to the ground station

# videostream vehicle: rpi takes picture with open cv, convert it to a jpg file to save trafic and sendig
# it in small junks to the ground sation trough the server. if video is not watched it's closed to save traffic

# server funktions as mittleman,sending everthing from the vehicle to the groundstaion
# and vice versa,constantly cheks for changed ip adresses from the vehicle and ground sation

password 		=b'rmxmjwby'			# for server authenication
address_server	=('217.61.120.98',3274)	# address server(ip and port), change to your own

import socket,threading,time,sys
#print('open-source project by www.OPEN-ATS.eu\nchange to your own IP and password')
if len(sys.argv) == 1: # checking for command line argument, if somethig autostart vehicle programs
	print('1) groundstation 2) server 3) vehicle')
	option_location = input('choose your location:') # option location
	if option_location != '2': #if server is chooesn, no need to ask which program anymore
		print('1) both 2) controlling 3) videostream')
		option_program = input('choose your program:') # option program
else:option_location = '3'; option_program = '1';

soc = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM) # internet protocol parameters
soc.sendto(b'',address_server)#before something can be received, something must be sent! (otherwise an error appears)
run=True #set variable to zero when porgrams should stop
keep_alive_message =b'a' #keep alive message
time_of_disconnect =0 #for stopping motor and videostream when disconnected

def sending_keepalive():#function, continuously sending keepalive messages, needed for stopping video stream and motors if disconected
	if option_location == '1':kafz = 0.05 #keep alive frequency, ground station needs to send kav more often than vehicle
	if option_location == '3':kafz = 1    #keep alive frequency, vehicle need to send kav more of than groundstation
	while run:
		soc.sendto(keep_alive_message + password,address_server) # keepalive message, "a" stands for "alive", an indication
		time.sleep(kafz)

def receiving_keepalive():#function, receiving keepalive messages, needed for stopping video stream and motors if disconnected
	global time_of_disconnect
	while run:msg=soc.recvfrom(655350)[0];time_of_disconnect=0

def count_time_diconnect(): # function, count 'time of disconnect' 
	global time_of_disconnect
	while run:time.sleep(0.05);time_of_disconnect+=1

def controll_window_and_send_data():#creat a controll window and send controll data
	import os; os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide' # annoying pygame support message
	import pygame; pygame.init() #import and init pygame to draw
	print('controlling groud station running')
	pygame.display.set_caption('controlling open-ats.eu')
	screen = pygame.display.set_mode((500,500))#create window 500x500 pixel big
	font = pygame.font.Font(pygame.font.get_default_font(),15) #for drawing fonts, dont use it inside loop, will slow down
	drag = False
	sc = 0 #send counter
	curx=cury=249
	pygame.mouse.set_cursor((24,24),(12,11),*pygame.cursors.compile((#drawing that cross shaped cursor
	"         XXXXXX         ","         X....X         ","          X..X          ","          X..X          ",
	"          X..X          ","          X..X          ","          X..X          ","          X..X          ",
	"XX        X..X        XX","X.XXXXXXXXX..XXXXXXXXX.X","X......................X","X......................X",
	"X.XXXXXXXXX..XXXXXXXXX.X","XX        X..X        XX","          X..X          ","          X..X          ",
	"          X..X          ","          X..X          ","          X..X          ","          X..X          ",
	"          X..X          ","          X..X          ","         X....X         ","         XXXXXX         ")))

	while run:
		time.sleep(0.0003)#needs to be faster than pygame event queue
		e = pygame.event.poll()#wait() for blocking element, e is a shortcut of event
		if e.type == pygame.QUIT:pygame.quit();break#clsoing pygame window;break so it doesnt continue and gives error
		if e.type == pygame.MOUSEBUTTONDOWN or e.type == pygame.MOUSEMOTION and drag:
			if   e.pos[0]<= 49:curx= 49#click outside border left
			elif e.pos[0]>=449:curx=449#click outside border right
			else:curx = e.pos[0]#click inside, equal mouse position
			if   e.pos[1]<= 49:cury= 49#click outside border up
			elif e.pos[1]>=449:cury=449#click outside border down
			else:cury = e.pos[1]#click inside, equal mouse position
			drag = True

		elif e.type == pygame.MOUSEBUTTONUP:#reset cursor when mousebutton release
			curx = cury = 249
			drag = False

		sc+=1
		if sc > 30: #not send as often as mouse input, saves traffic
			sc = 0
			mtr=round(-((cury-49-200)/200),3)#number between 1&-1
			svo=round( ((curx-49-200)/200),3)#number between 1&-1

			#important to do it on groundstation, so it can be edited while driving
			svo_r = int(round(svo*300+1550))#right servomotor
			svo_l = int(round(svo*300+1500))#left  servomotor
			mtr_r = int(round(mtr*200+1500))#right drive motors
			mtr_l = int(round(mtr*200+1500))#left  drive motors
			soc.sendto(('d ' + str(svo_r) + ' ' + str(svo_l) + ' ' + str(mtr_r)+ ' ' + str(mtr_l)).encode(),address_server)
			print(f"sent:    svo_r:{svo_r}  svo_l:{svo_l}  mtr_r:{mtr_r}  mtr_l:{mtr_l}")#just for testing, will slow down a bit
			screen.fill((0,0,0))
			pygame.draw.rect(screen,(20,20,20),(49,248,400,2))#cross flat 249 is the half -1 cause its 2 thick
			pygame.draw.rect(screen,(20,20,20),(248,49,2,400))#cross high 249 is the half -1 cause its 2 thick
			pygame.draw.rect(screen,((-mtr+1)/2*255/3,(mtr+1)/2*255/3,0),(47,47,404,404),4)#border
			pygame.draw.line(screen,((-mtr+1)/2*255/2,(mtr+1)/2*255/2,0),(248,248),(curx,cury),4)#draw thread
			pygame.draw.rect(screen,((-mtr+1)/2*255,  (mtr+1)/2*255,0)  ,(curx-40,cury- 2,80, 4))#draw cursor flat
			pygame.draw.rect(screen,((-mtr+1)/2*255,  (mtr+1)/2*255,0)  ,(curx- 2,cury-40, 4,80))#draw cursor high
			screen.blit(font.render(str(-svo),True,(100,100,100)),(170,30))#draw font
			screen.blit(font.render(str( mtr),True,(100,100,100)),(230,30))#draw font
			screen.blit(font.render(str( svo),True,(100,100,100)),(290,30))#draw font
			pygame.display.flip()#updates the screen

def receiv_and_display_video():#receiv image and display video
	print('videostream gound station running')
	print('waiting for images to be received')
	import cv2,io,numpy
	while run:#main loop, continuously receiving video data and diplaying them
		bytAry = bytearray()# byte array, where the image is saved
		while True:# loop where the individual packages are put together to form the picture
			part = soc.recvfrom(655350)[0] # wait for data to be received
			if part[:1] == b'v' or part[:1] == b'f':
				if part == b'f': # if no more data comes, an indication that the image ended
					#print('image received') # dont use it to often, will slow down program
					break  # breaks the loop 
				part =  part[1:]# removing first letter (identification)
				bytAry += part
		np_img = numpy.asarray(bytAry) # convert the input to an array
		try:
			aImg=cv2.imdecode(np_img, cv2.IMREAD_COLOR)
			aImg=cv2.resize(aImg,(640,360)) # downsize the image 
			aImg=cv2.flip(aImg,-1) # uncomment this for mirroring the image
			cv2.imshow('videostream', aImg) # first arg is the name of the window; dont displays the picture
			cv2.waitKey(10)#displays the picture, waits 10ms
		except:pass

def server(): #relay server
	print('server running')
	from datetime import datetime
	soc = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM) # internet protocol parameters 				why do i need this here!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	soc.bind(address_server) # address server (ip and port)
	adr_clt1 = adr_clt2 = ('0.0.0.0',5000) # address clients
	while run:
		msg, adr = soc.recvfrom(1024) # msg: reciving message, adr: incoming address
		if   adr == adr_clt1: soc.sendto(msg, adr_clt2)#; print('1'+str(msg))# for testing #sent msg to other client
		elif adr == adr_clt2: soc.sendto(msg, adr_clt1)#; print('2'+str(msg))# for testing #sent msg to other client
		elif msg == keep_alive_message +password: # only changing ip if authenticate with password 
			print(datetime.now().strftime("%d/%m/%Y %H:%M:%S")+' new login: '+str(adr))
			adr_clt2 = adr_clt1; adr_clt1 = adr # changing to new adresses

def receive_and_set_outputs():#receive control data_and_set_outputs of the raspbery pi
	print('controlling vehicle running')
	import os; os.system('sudo pigpiod /f >nul 2>&1')#starting GPIO deamon; suppress command line output
	time.sleep(1) # starting pigpiod takes a sec
	import pigpio # importing GPIO library os.system('clear')
	output = pigpio.pi().set_servo_pulsewidth # just shorting that long name

	def stop_motor_when_disconnected(): #cant use it in receive_and_set_outputs cause recvfrom (blocking element)
		while run:
			time.sleep(0.05)#needed, otherwise python will use all the ressources
			if time_of_disconnect > 5:
				# sending control data to the output GPIO pins
				output(15,1480)#drive motor, right in drive direction								change to new PINS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
				output(23,1480)#drive motor, left in drive direction
				print('\033[91mvehicle for 0.25s disconnected: motor stopped \033[0m') # \033[91m equals color red; \033[0m  equals color white
				time.sleep(3)

	threading.Thread(target = stop_motor_when_disconnected).start()

	cDa = [1500, 1500, 1500, 1500] # list with control data
	while run: # main loop, receiving control data and outputting them on the GPIO pins
		if time_of_disconnect <= 5: #under 250ms of diconnect the vehicle will contuine driving
			msg = soc.recvfrom(1024)[0]
			#print('received: ' + msg.decode()) #only for testing could slow down comunication
			if msg.decode()[0] =='d':# just real data is accepted and no alive data
				cDa = msg.split() # split data and put in list
				# sending control data to the output GPIO pins 
				output(14,int(cDa[1]))#steering motor, right in drive direction				change to new PINS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
				output(18,int(cDa[2]))#steering motor, left in drive direction
				output(15,int(cDa[3]))#drive motor,    right in drive direction
				output(23,int(cDa[4]))#drive motor,    left in drive direction


def record_and_send_video(): # function, record_and_send_video_stream
	print('videostream vehicle running')
	import cv2,numpy,io
	cap = cv2.VideoCapture(0) # 0 or 1, depending on whether you have one or more cameras
	# image size, 1280x720 or set to 320x180 to ensure lower quality continuous video stream
	cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)#image width,  dont go higher than 620 it will lag
	cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)#image height, dont go higher than 360 it will lag
	cap.set(cv2.CAP_PROP_FPS,          30)#fps
	cnt = 0 # image counter
	while run: # main loop, for continuously taking and sending video data
		if time_of_disconnect < 120:# six sec
			cnt += 1
			npImg = cap.read()[1] # capturing image

			## uncomment to save the images
			#cv2.imwrite("Images/Img"+str(cnt)+".jpg",npImg)

			# uncomment to show the image
			#cv2.imshow('stream',npImg) # 1st argument = window name
			#cv2.waitKey(1)

			npImg=cv2.resize(npImg,(320,180))# downsize the image for stream
			jImg = cv2.imencode('.jpg', npImg, [int(cv2.IMWRITE_JPEG_QUALITY),90])[1]# numpy image to jpg
			stream = io.BytesIO(jImg)# creating a stream to continously taking chunks from the jpg file
			while run:
				part = stream.read(504)# 506 is the max UDP package lengh, minus 2 for video authentification
				if not part: break# if-block will execute if string is empty; breaks the loop
				soc.sendto(b'v'+part,address_server)
			soc.sendto(b'f', address_server)# indication end of image, "f" stand for "finished frame"
			print('image sent ' + str(cnt))
		else:print('no connection to ground station, videostream paused');time.sleep(3)

if option_location == '1' or option_location == '3':#starting programme dependent which option was choosesn
	threading.Thread(target = sending_keepalive).start() # starting function keep alive
	if option_location == '1': # groundstation
		if option_program == '1' or option_program == '2': threading.Thread(target = controll_window_and_send_data).start()
		if option_program == '1' or option_program == '3': threading.Thread(target = receiv_and_display_video).start()
	if option_location == '3': #vehicle
		threading.Thread(target = receiving_keepalive).start()
		threading.Thread(target = count_time_diconnect).start() # needed for both: save videodata, shutfdown motors
		if option_program == '1' or option_program == '2': threading.Thread(target = receive_and_set_outputs).start()
		if option_program == '1' or option_program == '3': threading.Thread(target = record_and_send_video).start()
if option_location  == '2': threading.Thread(target = server).start()

input();print("exit program");run = False; exit();
# code maintained by Lukas Pfitscher & Spaltex (info@open-ats.eu)