

	#########################################
	#                                       #
	#           SETUP GUIDE                 #
	#                                       #
	#########################################
	
	The guide is split in three parts:
		1. 	Setup the controlling (steering, motor acceleration)
		2.	Setup the videostream
		3. 	Setup tmux and automation
		
	General:
	
	First of all you need to change to your own IP of your server on all programs.
	Just open them with a text editor. 
	
	The program name stands for: rpi = raspberry, lap = laptop, srv = server
	ctr = controlling, vid = videostream
	
	#########################################
	#        1. SETUP CONTROLLING           #
	#########################################
	
	To control the vehicle with a gamepad install pygame on your Laptop/PC with the command
	
		pip install pygame
		
	open the control-program (lap-ctr.py), do some stering with your gamepad, 
	if you see some data sending you did it right.
	
	Next, connect to your server via SSH, copy the controlling server program on your server
	and start the program by writing:
		
		python3 srv-ctr.py
		
	Again stere with your gamepad if you see the data arriving 
	on the server you did it again right
	
	Now log on to your Raspberry Pi and run the following command:
	
		python3 rpi-ctr.py
	
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
	All you need to do is start the program here. it could take up to 20 sec to start, 
	If you see a stream of "image send" you did it right.
	
		python3 rpi-vid.py
	
	Now you can start the server program

		python3 srv-vid.py
		
	and the video stream program on your laptop/pc.
	by click on "lap-vid.py"
	

	#########################################
	#    3. SETUP TMUX and AUTOAMATION      #
	#########################################
	
	You need tmux so your Python programs can run simultaneously and in the background.
	Install tmux on your Pi and server with the command:
	
		sudo apt install tmux
		
	With "Ctrl+C" you can close your programs like normally
	With "Ctrl+D" you can close a tmux session 
	
	We wrote start programs for the raspberry, the server and the laptop/pc
	It will automatically open tmux, split the sreen 
	and start the controlling and videostream programs.
	
	Just copy the start program to the folder where the other programs are and start it.
	
