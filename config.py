import os
import urllib2

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fjDpWQ34jfaI8aenC'

JSONRPC_LINK = 'http://localhost:6800/jsonrpc'

TOKEN = '3B4NzJn1niVKSEJPuGDY9YE//QMzw7F3oMQL455h+uM='

BASE_DIR = '/home/xerxes/ariadownloads'

opener = urllib2.build_opener()
opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
