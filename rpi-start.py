import time
time.sleep(20)      #because otherwise the program starts before rpi has internet and an error occurs with "try catch" might be better
import os           #importing os library so as to communicate with the system
os.system ("""tmux new-session -d -s ctr \; send-keys "python3 /home/pi/rpi-ctr.py" Enter \; split-window -h \; send-keys "python3 /home/pi/rpi-vid.py" Enter \; a""") #Launching GPIO library