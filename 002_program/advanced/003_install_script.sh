#!/bin/bash
# change password (security)
sudo usermod --password $(echo openats | openssl passwd -1 -stdin) pi

# add important aliases
echo "alias ll='ls -l'" >> ~/.bashrc
echo "alias la='ls -lA'" >> ~/.bashrc

# upgrade all packages, otherwise opencv wound work
sudo apt-get dist-upgrade -y

# install OpenCV
sudo apt install python3-opencv -y

# crontab -e
# @reboot sleep 60 && python3 /home/pi/start-vhc.py
# automatically edit crontab file ref: https://stackoverflow.com/a/9625233/13469595
(crontab -l 2>/dev/null; echo "@reboot sleep 30 && python3 /home/pi/start-vhc.py") | crontab -

# enable the camera module
echo "start_x=1" >> /boot/config.txt
# reboot to enable camera??
sudo reboot

# interface Options --> Camera --> enable
#raspistill -o image.jpg				will not work after crontab or vid running

# script maintained by Spaltex (spaltex@open-ats.eu)