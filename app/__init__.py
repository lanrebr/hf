from flask import Flask
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO
import os

app = Flask(__name__)
cfgname=os.environ.get('FLASK_CONFIG', 'development')
cfg = os.path.join(os.getcwd(), 'config', cfgname + '.py')
print(cfg)
app.config.from_pyfile(cfg)
bootstrap = Bootstrap(app)
socket = SocketIO(app)

from app import routes

socket.run(app)