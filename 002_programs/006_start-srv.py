import os
os.system("""tmux new-session -d -s ctr \; send-keys "python3 /root/srv.py" Enter \; a""")
