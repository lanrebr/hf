import os

basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = False
TESTING = False
IGNORE_AUTH = False
DROP_DB = True
SECRET_KEY = 'secret'
SERVER_NAME = 'localhost:3000'
MAX_CONTENT_LENGTH = 4*1024*1024*1024
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}