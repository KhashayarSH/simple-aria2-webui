import os
import urllib2

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
# Aria2 jsonrpc listening link
JSONRPC_LINK = 'http://localhost:6800/jsonrpc'

# Aria2 token for rpc comunication
TOKEN = 'Your_Token'

# Direction to which downloads will be downloaded
BASE_DIR = 'your/aria2/download/path'

# Opener used for rpc comunication
opener = urllib2.build_opener()
opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
