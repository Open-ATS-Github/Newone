import time
import os
os.system("""tmux new-session -d -s ctr \; send-keys "python3 /home/pi/ctr-vhc.py" Enter \; split-window -h \; send-keys "python3 /home/pi/vid-vhc.py" Enter \; a""")
