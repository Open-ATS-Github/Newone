	
	#########################################
	#		SETUP GUIDE						#
	#		www.Open-ATS.eu					#
	#########################################

	Here you can find all the programs to make your vehicle controlled over internet.
	There are two programs, one is for controlling the steering motors and the drive motors
	and the other program is responsible for transmitting video data over the internet.
	
	We are a talented group of free volunteers who are working hard
	to make this project available for everyone. If you find this helpful 
	consider donating or mention us if you implement the project into your own one.
	
	The guide is split into parts:
		1. 	Setup controlling (steering, drive)
		2.	Setup video stream
		3. 	Setup tmux and automation
		4.	Troubleshooting
		5.  Advanced stuff

	General: You need Python on the Laptop/PC for that 
	go to their website and download it there: www.python.org
	We tested everything on Raspberry Pi OS with desktop (release date: January 11th 2021).
	Only Raspbian (BUSTER) with desktop works, cause opencv has problems with other versions.
	On this version Python is preinstalled. 
	Same goes for the Server OS, if you use Debian 10, Python is pre-installed too.
	
	You need to change to your own IP of your server on all programs.
	Just open the "main.py" with a text editor and change to your own IP.
	
	#########################################
	#	1. SETUP CONTROLLING				#
	#########################################
	
	To control the vehicle with a your Mouse, install pygame on your Laptop/PC by typing into the cmd:
	
		pip3 install pygame
	
	open the "main.py" and choose groundstation as location and controlling as the subprogram. A window will apear, 
	you can now clic and drag the cross cursor, with this window u can later drive the vehicle
	
	Next, connect to your server via SSH, copy the server program on your server
	and start the program by writing:
	
		python3 main.py
	
	choose server as location, if you see a message with 'new login'
	on the server you did it right again.
	
	Now log on to your Raspberry Pi, copy the program and run it by writing:
	
		python3 main.py
		
	choose vehicle as location and controlling as subprogram.
	steer with your mouse, if you see the motors turning you are 
	done and you can start driving your vehicle.
	
	#########################################
	#	2. SETUP VIDEOSTREAM				#
	#########################################
	
	You need to enable the camera on your Raspberry Pi:
	
		sudo raspi-config
		
	Go to Interface Options --> Camera --> enable
	To check if the camera is working, type:
	
		raspistill -o image.jpg
	
	In addition, you need python3-opencv on your Raspberry Pi as well to get video input, 
	for this type in these two commands on your Raspberry Pi:
	
		sudo apt update
		sudo apt install python3-opencv -y    python3-opencv-headless
		
	You also need it on your laptop to output the video stream
	for that type into your cmd:
	
		pip install opencv-python
	
	Now log into your Raspberry Pi and copy the program on to your RPi
	All you need to do is to start the program here. It could take up to 20 sec to start, 
	If you see a stream of "image sent" you did it right.
	
		python3 main.py
	
	finally start the video stream program on your laptop/pc.
	
	#########################################
	#	3. SETUP TMUX and AUTOAMATION		#
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
	#	4. TROUBLESHOOTING					#
	#########################################
	
	Open the programs with a standard text editor here you can find to every code line a comment. 
	This is the most effective way to solve problems. 
	Read the FAQs (www.open-ats.eu/faq) it will answer some questions too. 

	#########################################
	#	5. ADVANCED STUFF					#
	#########################################

	we created shell scrips to speed up the hole installation process
	, look at the advanced folder. They aren't documented jet.

	Text maintained by Lukas Pfitscher (info@open-ats.eu)