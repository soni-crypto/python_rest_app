
from flask import current_app, render_template, json
from flask_socketio import SocketIO, join_room
from application.helpers.gestor_restaurant import ManagerData
from application.controllers.restaurant.orderDishes import Order
from application.controllers.restaurant.typeFoodABS import TypeFood_ABS
from application.controllers.restaurant.foodDishes import Food
from application.controllers.restaurant.commentsFood import CommentsFoodController
# from gevent import monkey
# monkey.patch_all()
socketio = SocketIO(cors_allowed_origins="*")
managerData = ManagerData()
@socketio.on("join_group_res_personalized")
def join_to_group(data):
    room = managerData.get_key_room_main()
    join_room(room)

@socketio.on("order_state_1")
def order_state_1(data):
    room_app = managerData.get_key_room_main()
    socketio.emit("message_order_state_1", json.dumps(data), room=room_app)
    
@socketio.on('order_state_21')
def order_state_21(data):
    room_app = managerData.get_key_room_main()
    socketio.emit("message_order_state_21", json.dumps(data), room=room_app)

@socketio.on('order_state_22')
def order_state_22(data):
    room_app = managerData.get_key_room_main()
    socketio.emit("message_order_state_22", json.dumps(data), room=room_app)

@socketio.on('order_state_3')
def order_state_3(data):
    room_app = managerData.get_key_room_main()
    socketio.emit("message_order_state_3", json.dumps(data), room=room_app)

@socketio.on('order_state_4')
def order_state_4(data):
    room_app = managerData.get_key_room_main()
    socketio.emit("message_order_state_4", json.dumps(data), room=room_app)

@socketio.on('order_state_6')
def decline_order(data):
    room_app = managerData.get_key_room_main()
    socketio.emit("message_order_state_6", json.dumps(data), room=room_app)
    