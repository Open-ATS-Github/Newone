

	#########################################
	#                                       #
	#           SETUP GUIDE                 #
	#		  www.Open-ATS.eu				#
	#                                       #
	#########################################
	
	The guide is split in three parts:
		1. 	Setup controlling (steering, motor acceleration)
		2.	Setup video stream
		3. 	Setup tmux and automation
		4.	Troubleshooting
		
	General:
	
	First of all, you need to change to your own IP of your server on all programs.
	Just open them with a text editor. 
	
	Only Raspbian with desktop works, cause open-cv has problems with the other version
	
	The program name stands for: vhc = vehicle, grs = ground station, srv = server
	ctr = controlling, vid = video stream
	
	#########################################
	#        1. SETUP CONTROLLING           #
	#########################################
	
	To control the vehicle with a gamepad, install pygame on your Laptop/PC with the command
	
		pip install pygame
		
	open the control-program (ctr-grs.py), do some steering with your gamepad, 
	if you see some data sending you did it right.
	
	Next, connect to your server via SSH, copy the controlling server program on your server
	and start the program by writing:
		
		python3 ctr-srv.py
		
	Again, stere with your gamepad if you see the data arriving 
	on the server you did it again right
	
	Now log on to your Raspberry Pi and run the following command:
	
		python3 ctr-vhc.py
	
	#########################################
	#       2. SETUP VIDEOSTREAM            #
	#########################################
	
	You need python3-opencv to get video input from your Raspberry Pi, 
	for that type in these two commands on your Raspberry Pi:
	
		sudo apt update
		sudo apt install python3-opencv 
		
	you also need it on your laptop to output the video stream
	for that go to the Opencv.org webpage.
	
	Now log in to your Raspberry Pi and copy the program on to your Pi
	All you need to do is start the program here. It could take up to 20 sec to start, 
	If you see a stream of "image sent" you did it right.
	
		python3 vid-vhc.py
	
	Now you can start the server program

		python3 vid-srv.py
		
	and the video stream program on your laptop/pc.
	by click on "vid-grs.py"
	

	#########################################
	#    3. SETUP TMUX and AUTOAMATION      #
	#########################################
	
	You need tmux so your Python programs can run simultaneously and in the background.
	Install tmux on your Pi and server with the command:
	
		sudo apt install tmux
		
	With "Ctrl+C" you can close your programs like normally.
	With "Ctrl+D" you can close a tmux session.
	
	We wrote start programs for the raspberry, the server and the laptop/pc
	It will automatically open tmux, split the screen 
	and start the controlling and video stream programs.
	
	Just copy the start program to the folder where the other programs are and start them.
	
	#########################################
	#    4. TROUBLESHOOTING					#
	#########################################
	
	Open the programs with a standard text editor here you can find to every code line a commend. 
	This is the most effective way to solve problems.
	