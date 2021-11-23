import os
os.system("""tmux new-session -d -s ctr \; send-keys "python3 ctr-grs.py" Enter \; split-window -h \; send-keys "python3 vid-grs.py" Enter \; a""")
#os.system("start cmd /k python ctr-grs.py") # for shity windows
#os.system("start cmd /k python vid-grs.py") # for shity windows
