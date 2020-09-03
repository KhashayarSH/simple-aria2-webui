import os
import urllib2

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fjDpWQ34jfaI8aenC'
# Aria2 jsonrpc listening link
JSONRPC_LINK = 'http://localhost:6800/jsonrpc'

# Aria2 token for rpc comunication
TOKEN = '3B4NzJn1niVKSEJPuGDY9YE//QMzw7F3oMQL455h+uM='

# Direction to which downloads will be downloaded
BASE_DIR = '/home/xerxes/ariadownloads'

# Opener used for rpc comunication
opener = urllib2.build_opener()
opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
