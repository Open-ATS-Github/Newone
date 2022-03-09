#!/bin/bash

# Generate new SSH key
ssh-keygen -t ed25519 -f ~/.ssh/id_rpi_car -P ""
ssh-copy-id -i ~/.ssh/id_rpi_car.pub Pi4overPhone

ssh Pi4overPhone "sudo apt-get update"
ssh Pi4overPhone "sudo apt-get install tmux vim -y"

# Copy script and files to RPi
scp install_script.sh Pi4overPhone:
scp start-vhc.py  Pi4overPhone:
scp ctr-vhc.py  Pi4overPhone:
scp vid-vhc.py  Pi4overPhone:
# Make the script executable
ssh Pi4overPhone "chmod u+x ~/install_script.sh"
# Start the script inside a new tmux session
ssh Pi4overPhone "tmux new-session -d -s my_session '~/install_script.sh'"

# script maintained by spaltex (spaltex@open-ats.eu)