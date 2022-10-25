    
  #########################################
  #        SETUP GUIDE                    #
  #        www.Open-ATS.eu                #
  #########################################

  Here you can find all the programs to make your vehicle accessible over internet.
  There are two programs, one is for controlling the steering motors and the drive motors
  and the other program is responsible for transmitting video data over the internet.
    
  The guide is split into parts:
     1. setup controlling (steering, drive)
     2. setup video stream
     3. setup tmux and automation
     4. troubleshooting
     5. advanced stuff

  General: You need Python on the Laptop/PC for that 
  go to their website and download it there: www.python.org
  
  Raspberry Pi OS Lite (32-bit,Release: 2022-04-04)
  A port of Debian Bullseye with no desktop environment
  Testet on Raspberry Pi Zero 2 and Raspberry Pi 4

  On this version Python is preinstalled.
  Same goes for the Server OS, if you use Debian 10, Python is pre-installed too.
    
  You need to change to your own IP of your server and passwort.
  Just open the "main.py" with a text editor and change to your own IP.
    
  #########################################
  #    1. SETUP CONTROLLING               #
  #########################################
  
  To control the vehicle with a your Mouse, install pygame on your Laptop/PC by typing into the cmd:

      pip3 install pygame

  Open the "main.py" with your Laptop/PC and choose groundstation as location and controlling as the subprogram.
  A window will appear, you can now click and drag the cross cursor, with this window you can drive the vehicle
  (drag right, left for sterreing; forwart to accelarete; back for break).
    
  Next open the server program on your Laptop/PC for testing localy in your WiFi or 
  connect to your server via SSH, copy the main.py program on your server
  and start the program by writing for testing it over mobile internet:

      python3 main.py

  Choose server as location, if you see a message with 'new login'
  on the server you did it right again.
    
  Now log on to your Raspberry Pi, install GPIO library
    
      sudo apt-get install pigpio -y
      sudo apt-get install python3-pigpio -y
    
  Copy the program on to you Pi and run it by writing:

      python3 main.py

  Choose "vehicle" as location and "controlling" as subprogram.
  steer with your mouse, if you see the motors turning you are 
  done and you can start driving your vehicle.
  
  #########################################
  #    2. SETUP VIDEOSTREAM               #
  #########################################
  
  To test the videostream you don't need to have a raspberry pi nor a server.
  You can test it all on your laptop/PC just open the programs on your laptop/PC
  (vehicle videostream, server and groundstation videostream). 
    
  You need to enable the old camera driver on your RPi 
  because the new drive doesn't support OpenCV yet:

        sudo raspi-config

  Go to Interface Options --> Legacy Camera --> enable
  To check if the camera is working, type:
    
      raspistill -o image.jpg
    
  In addition, you need python3-opencv on your RPi as well to get video input, 
  for this type in these two commands on your Raspberry Pi:
    
      sudo apt update
      sudo apt install python3-opencv -y

  You also need it on your laptop to output the videostream
  for that type into your cmd:

      pip3 install opencv-python

  Copy the program on your RPi and start it.
  
      python3 main.py
  
  Choose "vehicle" as location and "videostream" as subprogram.
  It could take up to 10 sec to start, If you see a stream 
  of "image sent" you did it right.
  
  Finally start the video stream program on your laptop/PC by writing:
  
      python3 main.py
   
   Choose "groundstation" as location and "videostream" as subprogram.
   If a window apears with a videostream you are done.
  
  #########################################
  #    3. SETUP TMUX and AUTOMATION       #
  #########################################
  
  Tmux is needed so the Python programs can run simultaneously and in the background.
  Install tmux on the Pi and server with the command:
  
      sudo apt install tmux -y
      
  With "Ctrl+C" you can close the programs like normally.
  With "Ctrl+D" you can close a tmux session.
  
  We wrote start programs for the raspberry, and the laptop/pc
  It will automatically open tmux, split the screen 
  and start the controlling and video stream programs.
  
  Just copy the start programs to the folder where the other programs are and start theme there.
  
  #########################################
  #    4. TROUBLESHOOTING                 #
  #########################################
  
  Open the programs with a standard text editor here you can find to every code line a comment. 
  This is the most effective way to solve problems.
  If you realy strugl at something (more than 1h), you can also write us an email and we can help.
  Read the FAQs (www.open-ats.eu/faq) it will answer some questions too.

  #########################################
  #    5. ADVANCED STUFF                  #
  #########################################

  We created shell scripts to speed up the hole installation process,
  look at the advanced folder. They aren't documented jet.

  We are a talented group of free volunteers who are working hard
  to make this project available for everyone. If you find this helpful 
  consider donating or mention us if you implement the project into your own one.
  Text maintained by Lukas Pfitscher (info@open-ats.eu)