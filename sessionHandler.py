from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS, cross_origin
import threading
import time

app = Flask(__name__)
cors = CORS(app)
socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")
app.config['CORS_HEADERS'] = 'Content-Type'

i = 0

connected = False

def incrementHandler():
	global connected
	global i
	while connected:
		i += 1
		time.sleep(0.1)
		print(i)
		socketio.emit('currentSession', {'data': str(i)})

@cross_origin()
@socketio.on('connect')
def connect(auth):
	global connected
	socketio.emit('currentStatus', {'data': 'Connected'})
	connected = True
	thread = threading.Thread(target=incrementHandler)
	thread.start()


@cross_origin()
@socketio.on('disconnect')
def disconnect():
	global i
	global connected
	print('Client disconnected')
	i = 0
	connected = False

@cross_origin()
@app.route('/')
def index():
	return 'Hello World!'
