# simple-aria2-webui

# Introduction
A simple WebUI for Aria2 Download Utility with an implemented Download Queue feature to start and stop downloads at certain times of the day. It can be used as a local Remote download server running on a device like raspberry pi and accessed by other devices in the local network.

# Features
1. Essential Aria2 functionalities
2. Download Queues
3. Responsive design, supporting desktop and mobile devices due to Bootstrap framework
4. User-Friendly UI
    * Download progress bar for each download
    * Useful information for downloads(Download Rate, Number of Connections, Queue Name, ...)
    * Filters to display certain downloads
    * A page to access Aria2's download directory(Useful when used as download server)

# Screenshots
![Image](https://raw.githubusercontent.com/KhashayarSH/simple-aria2-webui/master/screenshots/index.png)

![Image](https://raw.githubusercontent.com/KhashayarSH/simple-aria2-webui/master/screenshots/add_download.png)

![Image](https://raw.githubusercontent.com/KhashayarSH/simple-aria2-webui/master/screenshots/downloads.png)

![Image](https://raw.githubusercontent.com/KhashayarSH/simple-aria2-webui/master/screenshots/queues.png)

# Prerequisites
* Aria2 Download Utility [Link](https://aria2.github.io/)
* Python 2 and used packages

# Installation
## Install Aria2
You need to setup your Aria2 first install it with:
'''bash
sudo apt install aria2
'''
## Aria2 configuration
Create a new configuration file *aria2.conf* with following content:

'''
##files
dir=/path/to/downloads
file-allocation=falloc
continue=true
daemon=true
disk-cache=32M

##logging
log=/path/to/aria2.log
console-log-level=warn
log-level=notice

##downloads
max-concurrent-downloads=5
max-connection-per-server=5
min-split-size=20M
split=4
disable-ipv6=true

##sessions
force-save=true
input-file=/path/to/aria2.session
save-session=/path/to/aria2.session
save-session-interval=10

##security
http-auth-challenge=true
check-certificate=false
enable-rpc=true
rpc-listen-all=true
rpc-secret=*YOUR TOKEN*

#rpc-secure=true
#rpc-allow-origin-all=true
#rpc-certificate=/youruser/aria2/cet/aria2.pfx

##ports
rpc-listen-port=6800

##others
summary-interval=120
enable-dht=true

##times
timeout=600
retry-wait=30
max-tries=50
'''

Now set the new *aria2.conf* as the new configuration with following command:
'''bash
sudo aria2c --conf-path="/path/to/aria2.conf"
'''

## Add Aria2 as a systemd service
Add Aria2 as a systemd service by pasting following content in *aria2.service*:

'''bash
sudo nano /lib/systemd/system/service/aria2.service
'''

'''
[Unit]
Description=Aria2c download manager
Requires=network.target
After=dhcpcd.service

[Service]
Type=forking
User=*youruser*
RemainAfterExit=yes
ExecStart=/usr/bin/aria2c --conf-path=/path/to/aria2.conf
ExecReload=/usr/bin/kill -HUP $MAINPID
ExecStop=/usr/bin/kill -s STOP $MAINPID
RestartSec=1min
Restart=on-failure

[Install]
WantedBy=multi-user.target
'''

Restart and now you can start Aria2 service with:
'''bash
sudo service aria2 start
'''
You can check status with:
'''bash
sudo service aria2 status
'''
## Set config.py
Replace *'your_secret_key'*, *'aria2_token'* and *'/path/to/downloads'* with appropriate values.
'''python
import os
import urllib2

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
# Aria2 jsonrpc listening link
JSONRPC_LINK = 'http://localhost:6800/jsonrpc'

# Aria2 token for rpc comunication
TOKEN = 'aria2_token'

# Direction to which downloads will be downloaded
BASE_DIR = '/path/to/downloads'

# Opener used for rpc comunication
opener = urllib2.build_opener()
opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
'''
## Run Flask
In project directory run flask with following commands:
'''bash
export FLASK_APP=aria2\ webui.py
flask run
'''
# License
[link](https://raw.githubusercontent.com/KhashayarSH/simple-aria2-webui/master/LICENSE)
