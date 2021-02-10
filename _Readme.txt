

	#########################################
	#                                       #
	#           SETUP GUIDE                 #
	#                                       #
	#########################################
	
	The guide is split in three parts:
		1. 	setup the controlling (steerring, motor acceleration)
		2.	setup the videostream
		3. 	setup tmux and automation
		
	General:
	
	First of all you need to change to your own IP of your server on all programs.
	Just open them with a text editor. 
	
	The program name stands for: rpi = raspberry, lap = laptop, srv = server
	ctr = controlling, vid = videostream
	
	#########################################
	#        1. SETUP CONTROLING            #
	#########################################
	
	To control the vehicle with a gamepad install pygame on your Laptop/PC with the comand
	
		pip install pygame
		
	open the control-program (lap-ctr.py), do some stering with your gamepad, 
	if you see some data sending you did it right.
	
	Next go to your server, copy the controlling server programm on your server
	and start the programm by writing:
		
		python3 srv-ctr.py
		
	Again stere with your gamepad if you see the data ariving 
	on the server you did it again right
	
	Now log on to your Raspberry Pi, all you need to do is start the program here, write:
	
		python3 rpi-ctr.py
	
	#########################################
	#       2. SETUP VIDEOSTREAM            #
	#########################################
	
	You need python3-opencv to get video input from your Raspberry Pi, 
	for that type in these two commands on your Raspberry Pi:
	
		sudo apt update
		sudo apt install python3-opencv 
		
	you also need it on your laptop to output the videostream
	for that go to the Opencv.org webpage.
	
	Now log in to your Raspberry Pi and copy the program on to your Pi
	All you need to do is start the program here. it could take up to 20 sec to start, 
	If you see a stream of "image send" you did it right.
	of corse the camera has to be conected
	
		python3 rpi-vid.py
	
	Now you can start the server program

		python3 srv-vid.py
		
	and the video stream program on your laptop/pc.
	by klick on "lap-vid.py"
	

	#########################################
	#    3. SETUP TMUX and AUTOAMATION      #
	#########################################
	
	You need Tmux so your Python programms can work simultaniosly and in the background.
	Install Tmux on your Pi and server with the command:
	
		sudo apt install tmux
		
	With "Strg+c" you can close your programs like normaly
	With "Strg+d" you can close a tmux session 
	
	We wrote start programms for the raspberry, the server and the laptop/pc
	It will autmaticly open tmux, split the sreen 
	and starts the controlling and videostream programs.
	
	Just copy the start programm to the folder where the other programms are and start it.
	
	
	


		
	