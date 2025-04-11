from flask import current_app
from application.models.Restaurant import OrderDishes, db
from application.helpers.gestor_restaurant import ManagerData
from application.controllers.restaurant.foodDishes import Food
from application.controllers.restaurant.waitressController import WaitressMainC
from application.controllers.restaurant.userController import UsersAdmin
from application.controllers.restaurant.historyController import StockHistoryC
from sqlalchemy import desc, or_
from application.controllers.restaurant.configurationDataController import ConfigurationDataController
import pytz

managerData = ManagerData()
recordModel = StockHistoryC()
foodController = Food()
waitressController = WaitressMainC()
adminsController = UsersAdmin()
configurationDataController = ConfigurationDataController()

class Order:
    app=None
    def __init__(self):
        self.app = current_app

    def get_all_free(self, d_json):
        try:
            query = OrderDishes.query
            if "id" in d_json.keys():
                query = query.filter(OrderDishes.id == d_json["id"])
            if "date_start" in d_json.keys():
                query = query.filter(OrderDishes.created_at >= d_json["date_start"])
            if "date_end" in d_json.keys():
                query = query.filter(OrderDishes.created_at <= d_json["date_end"])
            if "state_order" in d_json.keys():
                if isinstance(d_json["state_order"], list):
                    query = query.filter(or_(*[OrderDishes.state_order == state for state in d_json["state_order"]]))
                else:
                    query = query.filter(OrderDishes.state_order == d_json["state_order"])
            if "id_user_admin" in d_json.keys():
                query = query.filter(OrderDishes.id_user_admin == d_json["id_user_admin"])
            if "id_user_context" in d_json.keys():
                query = query.filter(OrderDishes.id_user_context == d_json["id_user_context"])
            if "id_table" in d_json.keys():
                query = query.filter(OrderDishes.id_table == d_json["id_table"])
            if "user_level" in d_json.keys():
                query = query.filter(OrderDishes.user_level == d_json["user_level"])
            if "desc" in d_json.keys():
                query = query.order_by(desc(OrderDishes.id))

            if "date_end" not in d_json.keys() and "date_start" not in d_json.keys(): 
                data = query.limit(15).all()
            if "limit" in d_json.keys():
                data = query.limit(d_json["limit"]).all()
            else:
                data = query.limit(50).all()
            id_admin_temp = 0
            for d in data:
                if d.id_user_admin != id_admin_temp:
                    id_admin_temp = d.id_user_admin
                dataConfigAdmin = configurationDataController.read({"id_admin":id_admin_temp})[0]
                time_zone = pytz.timezone(dataConfigAdmin.time_zone) 
                d.created_at = d.created_at.astimezone(time_zone)
                
            return data
        except Exception as error:
            print("Error: ", error)
            return []
            
    def insert(self, data):
        state_order = data["state_order"]
        id_user_admin = data["id_user_admin"]
        id_user_context = data["id_user_context"]
        user_level = data["user_level"]
        order_code = data["order_code"]
        id_table = data["id_table"]
        
        prepared_data = OrderDishes(
                state_order=state_order,
                id_user_admin = id_user_admin,
                id_user_context = id_user_context,
                order_code = order_code,
                user_level = user_level,
                id_table = id_table,
            )
        
        db.session.add(prepared_data)
        db.session.commit()
        return prepared_data
    
    def delete(self, data_filter):
        id_user_context = managerData.email_to_id_admin()
        
        query = OrderDishes.query
        if "id" in data_filter.keys():
            query = query.filter(OrderDishes.id == data_filter["id"])
        if "id_user_admin" in data_filter.keys():
            query = query.filter(OrderDishes.id_user_admin == data_filter["id_user_admin"])
        if "id_table" in data_filter.keys():                
            query = query.filter(OrderDishes.id_table == data_filter["id_table"])
        
        fila = query.filter(OrderDishes.id_user_admin == id_user_context).all()
        for f in fila:
            db.session.delete(f)
        db.session.commit()
        return fila
    
    def update(self, id, data):
        response = OrderDishes.query.filter(OrderDishes.id == id, OrderDishes.id_user_admin == data["id_admin"]).first()
        del(data["id_admin"])
        if response:
            for key, value in data.items():
                setattr(response, key, value)
        db.session.commit()
            
        return response
    
    def update_status(self, id, state_order = 1):
        id_user_context = managerData.email_to_id_admin()
        response = OrderDishes.query.filter(OrderDishes.id == id, OrderDishes.id_user_admin == id_user_context).first()
        if response != None:
            response.state_order = state_order
        
        db.session.commit()
            
        return {"status":200}
    
                
            
            
            