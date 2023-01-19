#!/usr/bin/env python3

#this is a program for controlling a vehicle over mobile internet (videostream and controlling motors)
#there are actually 3 programs in this single file for the groundstation, server and vehicle

###short description of the individual subprograms

#controlling ground station: reads the input of the joystick and sends it to the vehicle through the server
#continuously send "keep alive" to make the vehicle stop when disconnected

#videostream ground station: receives the image from the vehicle in junks, recombines it to a full image and displays it
#sending alive messages so the vehicle wouldn't send when the ground station isnt open to save traffic

#controlling vehicle: receiving control data from the ground station through the server and sets the outputs of the pi accordingly
#vehicle will stop if there is no connection to the ground station

#videostream vehicle: rpi takes picture with open cv, convert it to a webp file to save traffic and sending
#it in small junks to the ground station through the server. if video is not watched it's closed to save traffic

#server functions as mittleman,sending everything from the vehicle to the ground station
#and vice versa,constantly checks for changed ip addresses from the vehicle and ground sation

password = b'rmxmjwby'#for a secure communication, change to your own (for server authentication)
address_server = ('127.0.0.1',3274)#address server(ip and port), change to your own
print('open-source project by www.OPEN-ATS.eu\nchange to your own IP and password')

import socket,threading,time,sys

if len(sys.argv) > 1:#if sysargs are given, use them
  option_location = sys.argv[1];#option location
  option_program  = sys.argv[2];#option program
else:#checking for command line arguments, if something autostart vehicle programs
  print('choose your location: 1) ground station 2) server 3) vehicle');  option_location = input()
  if option_location != '2':#if server is chosen, no need to ask which program anymore
    print('choose your program: 1) both 2) controlling 3) videostream'); option_program = input()

soc = socket.socket(family = socket.AF_INET,type=socket.SOCK_DGRAM)#internet protocol parameters
soc.sendto(b'',address_server)#before something can be received, something must be sent! (otherwise an error appears)
run=True#set variable to zero when all programs should stop
keep_alive_message =b'\xff'#keep alive message (number \xff = 255)
time_of_disconnect =0#for stopping motor and videostream when disconnected

def sending_keepalive():#function, continuously sending keepalive messages, needed for stopping video stream and motors if disconnected
  if option_location =='1':kafz=0.05 #keep alive send interval, ground station needs to send kav more often than vehicle
  if option_location =='3':kafz=1    #keep alive send interval, vehicle needs to send kav more often than ground station
  while run:
    soc.sendto(keep_alive_message + password,address_server) # keepalive message, "a" stands for "alive", an indication
    time.sleep(kafz)

def receiving_keepalive():#function, receiving keepalive messages, needed for stopping video stream and motors if disconnected
  global time_of_disconnect
  while run:msg=soc.recvfrom(655350)[0];time_of_disconnect=0;time.sleep(0.05);#sleep needed so it's not checking for every incomming msg

def count_time_disconnect():#function, count 'time of disconnect' 
  global time_of_disconnect
  while run:time.sleep(0.05);time_of_disconnect+=1#increase by one every 50ms

def control_window_and_send_data():#create a control window and send control data
  import os; os.environ['PYGAME_HIDE_SUPPORT_PROMPT']='hide'#hide annoying pygame support message
  import pygame; pygame.init() #import and init pygame to draw
  print('controlling groud station running')
  pygame.display.set_caption('controlling open-ats.eu')
  screen = pygame.display.set_mode((500,500))#create window 500x500 pixel big
  font = pygame.font.Font(pygame.font.get_default_font(),15)#for drawing fonts, dont use it inside loop, will slow down
  mousebuttondown = False
  sc=0#speed counter
  curx=cury=249#virtual joystick position
  pygame.mouse.set_cursor(pygame.cursors.broken_x)#set cursor to x-shape, just looks better
  
  while run:
    time.sleep(0.0003)#needs to be faster than pygame event queue
    e = pygame.event.poll()#wait() for blocking element, e is a shortcut of event
    if e.type == pygame.QUIT:pygame.quit();break#closing pygame window;break, so it doesnt continue and gives error
    if e.type == pygame.MOUSEBUTTONDOWN or e.type == pygame.MOUSEMOTION and mousebuttondown: #"and" has priority before "or"
      if   e.pos[0]<= 49:curx= 49#click outside border left
      elif e.pos[0]>=449:curx=449#click outside border right
      else:curx = e.pos[0]#click inside, equal mouse position
      if   e.pos[1]<= 49:cury= 49#click outside border up
      elif e.pos[1]>=449:cury=449#click outside border down
      else:cury = e.pos[1]#click inside, equal mouse position
      mousebuttondown = True
    
    elif e.type ==pygame.MOUSEBUTTONUP:#reset virtual joystick when mouse button is released
      curx = cury = 249;mousebuttondown=False
    
    #drawing virtual joystick
    sc+=1#speed counter
    if sc > 30:#not send as often as mouse input, saves traffic
      sc=0
      #convert joystick input 49-449 to a number between 1&-1, so it's easier work with
      mtr=round(-((cury-49-200)/200),3)
      svo=round( ((curx-49-200)/200),3)
      
      #good to do it on ground station, so it can be edited while driving
      #convert 1&-1 to a number between 1250-1850
      svo_r=int(round(svo*300+1550))#right servomotor
      svo_l=int(round(svo*300+1500))#left  servomotor
      mtr_r=int(round(mtr*200+1500))#right drive motors
      mtr_l=int(round(mtr*200+1500))#left  drive motors
      soc.sendto(b'\xfe'+(' ' + str(svo_r)+' '+ str(svo_l)+' '+str(mtr_r)+' '+str(mtr_l)).encode(),address_server)#fe equals for 254
      print(f"sent:    svo_r:{svo_r}  svo_l:{svo_l}  mtr_r:{mtr_r}  mtr_l:{mtr_l}")#just for testing, will slow down a bit
      screen.fill((0,0,0))
      clr_r = (-mtr+1)/2*255#color red
      clr_g = ( mtr+1)/2*255#color green
      pygame.draw.rect(screen,(20,20,20),(49,248,400,2))#cross flat 249 is the half -1 cause its 2 thick
      pygame.draw.rect(screen,(20,20,20),(248,49,2,400))#cross high 249 is the half -1 cause its 2 thick
      pygame.draw.rect(screen,(clr_r/3,clr_g/3,0),(47,47,404,404),4)#border
      pygame.draw.line(screen,(clr_r/2,clr_g/2,0),(248,248),(curx,cury),4)#draw thread
      pygame.draw.rect(screen,(clr_r,clr_g,0),(curx-40,cury- 2,80, 4))#draw cursor flat
      pygame.draw.rect(screen,(clr_r,clr_g,0),(curx- 2,cury-40, 4,80))#draw cursor high
      screen.blit(font.render(str(-svo),True,(100,100,100)),(170,30))#draw turning left  angle as text between -1 and 1
      screen.blit(font.render(str( svo),True,(100,100,100)),(290,30))#draw turning right angle as text between -1 and 1
      screen.blit(font.render(str( mtr),True,(100,100,100)),(230,30))#draw motor power as text
      pygame.display.flip()#updates the screen

def receive_and_set_outputs():#receive control data_and_set_outputs of the raspberry pi
  print('controlling vehicle running')
  import os; os.system('sudo pigpiod /f >nul 2>&1')#starting GPIO daemon; suppress command line output
  time.sleep(1)#starting pigpio takes a sec
  import pigpio#importing GPIO library os.system('clear')
  output = pigpio.pi().set_servo_pulsewidth#just shorting that long name

  def stop_motor_when_disconnected():#cant use it in receive_and_set_outputs cause recvfrom (blocking element)
    while run:
      time.sleep(0.05)
      if time_of_disconnect>5:#sending control data to the output GPIO pins
        output(15,1480)#drive motor, right in drive direction
        output(23,1480)#drive motor, left  in drive direction
        print('\033[91m'+'vehicle for 0.25s disconnected: motor stopped'+'\033[0m') #\033[91m equals color red; \033[0m  equals color white
        time.sleep(3)
  threading.Thread(target = stop_motor_when_disconnected).start()
  
  cDa = [1500,1500,1500,1500]#list with control data
  while run:#main loop, receiving control data and outputting them on the GPIO pins
    if time_of_disconnect <= 5:#under 250ms of disconnect the vehicle will continue driving
      msg = soc.recvfrom(1024)[0]
      #print('received: '+msg.decode()) #only for testing could slow down communication
      if msg.decode()[0]==b'\xfe':# just real data is accepted and no alive data
        cDa = msg.split()#split data and put in list
        #sending control data to the output GPIO pins 
        output(14,int(cDa[1]))#steering motor, right in drive direction
        output(18,int(cDa[2]))#steering motor, left  in drive direction
        output(15,int(cDa[3]))#drive    motor, right in drive direction
        output(23,int(cDa[4]))#drive    motor, left  in drive direction

def record_and_send_video():#function, record_and_send_video_stream
  print('videostream vehicle running')
  import cv2,numpy
  cap = cv2.VideoCapture(0) #0 or 1, depending on whether you have one or more cameras
  #image size, 1280x720 or set to 320x180 to ensure lower quality continuous video stream
  cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)#image width,  dont go higher than 640 it will lag
  cap.set(cv2.CAP_PROP_FRAME_HEIGHT,180)#image height, dont go higher than 360 it will lag
  cap.set(cv2.CAP_PROP_FPS,          30)#fps
  cnt  =0#image counter
  tilex=4#count tiles in x
  tiley=2#count tiles in y
  previous_img = numpy.empty((2,4,90,80,3),dtype=numpy.uint8) #array for tiles
  
  #function numpy.uint8(x<y) will give 0 or 1 => 1 or 255 
  #def sumabsdiff(img1,img2): return numpy.sum((img1-img2)*(numpy.uint8(img1<img2)*254+1))
  #def brightnessup(img1,img2): return numpy.sum(numpy.uint8(img1>img2)*1)
  #def brightnessdn(img1,img2): return numpy.sum(numpy.uint8(img1<img2)*1)
  
  def sumabsdiff(img1,img2): return numpy.sum(numpy.uint8(img1>(img2+2))*(img1-img2)+(numpy.uint8(img2>(img1+2)))*(img2-img1))
  
  while run:#main loop, for continuously taking and sending video data
    if time_of_disconnect < 120: #six sec
      img=cap.read()[1] #capturing numpy image
      
      #uncomment to save image
      #cv2.imwrite("images/img"+str(cnt)+".webp",img)
      #uncomment to show image
      #cv2.imshow('stream',img) # 1st argument: window title
      #cv2.waitKey(1)
      
      img=cv2.resize(img,(320,180))# downsize the image for stream, (if resolution is changes webp header needs to change)
      img=img.reshape(tiley,int(img.shape[0]/tiley),tilex,int(img.shape[1]/tilex),3).swapaxes(1,2) #convert to blocks, first y, second x, resuolution:80:90
      for id_img_row, img_row in enumerate(img):
        for id_img_tile, img_tile in enumerate(img_row):
          #if brightnessup(previous_img[id_img_row,id_img_tile],img_tile) > 
          if sumabsdiff(previous_img[id_img_row,id_img_tile],img_tile) > 500: # 80*90*3 = 21600 is 1%
            #print(str(id_img_row)+' '+str(id_img_tile)+' '+str(sumabsdiff(previous_img[id_img_row,id_img_tile],img_tile)))
            
            webp_image = (cv2.imencode('.webp',img_tile,[int(cv2.IMWRITE_WEBP_QUALITY),90])[1]) #convert to webp
            udp_packages = numpy.array_split(webp_image,len(webp_image)/500+1) #split into 500 byte chunks
            for package in udp_packages:
              
              cnt += 1
              #print('tile sent '+str(cnt)+' '+str(id_img_tile+id_img_row*4)+' '+str(sumabsdiff(previous_img[id_img_row,id_img_tile],img_tile)))
              #time.sleep(0.1)
              
              soc.sendto(((id_img_tile+id_img_row*4).to_bytes(1,'big')+package.tobytes()),address_server)
      previous_img = img
    else:print('vehicle for    3s disconnected: videostream paused');time.sleep(3)

def receive_and_display_video():#receive and display image
  print('videostream ground station running')
  print('waiting for images to be received')
  import cv2,numpy
  
  img = bytearray()#incoming image data is saved
  np_tile = [numpy.empty((90,80,3),dtype=numpy.uint8)]*8
  pervious_index = 0
  while run:#main loop, continuously receiving video data and displaying it
    package = soc.recvfrom(655350)[0]#wait for data to be received
    index = int.from_bytes(package[:1],'big')#first byte: package identification
    if index < 8:#check for video data
      #print(index)
      if pervious_index != index:#new tile
        webp_tile = numpy.frombuffer(img, dtype=numpy.uint8)#add head, tail
        try:
         np_tile[pervious_index] = cv2.imdecode(webp_tile,cv2.IMREAD_COLOR)#webp to np
         if pervious_index > index:#only show pic if all tiles are send 
           img_t  =numpy.concatenate((np_tile[0:4]),axis=1)#reassemble image together horizontally
           img_d  =numpy.concatenate((np_tile[4:8]),axis=1)#reassemble image together vertically
           img_al =numpy.concatenate((img_t,img_d)) #list of numpy arrays into single numpy array
           img_al =cv2.resize(img_al,(640,360))#upscale the image to get a better view
           cv2.imshow('videostream Open-ATS',img_al) #first arg is the name of the window; dont displays the picture
           cv2.waitKey(1)#displays the picture, waits 1ms
        except:print('failed');pass;
        img = bytearray()#reset img for next tile
      pervious_index = index
      img = img + package[1:]

def server(): #relay server
  print('server running')
  from datetime import datetime
  soc = socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM)#internet protocol parameters  why do i need this here?
  soc.bind(address_server)#address server (ip and port)
  adr_clt1 = adr_clt2 = ('0.0.0.0',5000)#address clients
  while run:
    msg, adr = soc.recvfrom(1024)#msg: receiving message, adr: incoming address
    #forward the message to the other client
    if   adr == adr_clt1: soc.sendto(msg, adr_clt2)#;print('1'+str(msg))# for testing #sent msg to other client
    elif adr == adr_clt2: soc.sendto(msg, adr_clt1)#;print('2'+str(msg))# for testing #sent msg to other client
    elif msg == keep_alive_message +password:#check for a keep-alive message with the correct password
      print(datetime.now().strftime("%d/%m/%Y %H:%M:%S")+' new login: '+str(adr))#for differentiating new logins, cause server will run all time
      adr_clt2 = adr_clt1 #update the client addresses
      adr_clt1 = adr

#starting programms, dependents which option was chosen
if option_location    =='1' or option_location =='3':
  threading.Thread(target = sending_keepalive).start()#starting function: keep alive
  if option_location  =='1':#ground station
    if option_program =='1' or option_program  =='2':threading.Thread(target = control_window_and_send_data).start()
    if option_program =='1' or option_program  =='3':threading.Thread(target = receive_and_display_video).start()
  if option_location  =='3':#vehicle
    threading.Thread(target = receiving_keepalive).start()
    threading.Thread(target = count_time_disconnect).start()#needed for both: save videodata, shutdown motors when diconected
    if option_program =='1' or option_program  =='2':threading.Thread(target = receive_and_set_outputs).start()
    if option_program =='1' or option_program  =='3':threading.Thread(target = record_and_send_video).start()
if option_location    =='2':threading.Thread(target = server).start()#start server

input();print('exit program');run=False;exit();
#code maintained by Lukas Pfitscher & Spaltex (info@open-ats.eu)