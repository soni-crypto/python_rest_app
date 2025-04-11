# from flask_socketio import SocketIO
from application.main import app
from application.helpers.sockets_order import socketio
from flask_cors import CORS


app.config['SECRET_KEY'] = 'secret!'
CORS(app, resources={r"/*": {"origins": "*"}})
socketio.init_app(app, async_mode='gevent')
if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000, host="0.0.0.0")
    # app.run(debug=True, port=5000, host="0.0.0.0")