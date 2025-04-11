from flask import current_app
from application.models.Restaurant import DataOrder, db
from application.helpers.gestor_restaurant import ManagerData
from application.controllers.restaurant.foodDishes import Food
from application.controllers.restaurant.waitressController import WaitressMainC
from application.controllers.restaurant.userController import UsersAdmin
from sqlalchemy import desc

managerData = ManagerData()
foodController = Food()
waitressController = WaitressMainC()
adminsController = UsersAdmin()

class DataOrderController:
    app=None
    def __init__(self):
        self.app = current_app

    def read(self, data_json):
        try:
            ctn=[]
            query = DataOrder.query
            keys = data_json.keys()
            if "id" in keys:
                query = query.filter(DataOrder.id == data_json["id"])
            if "id_admin" in keys:
                query = query.filter(DataOrder.id_admin == data_json["id_admin"])
        
            data = query.order_by(desc(DataOrder.id)).all()
            for i in data:
                data_temp = i.__dict__
                del(data_temp["_sa_instance_state"])
                del(data_temp["updated_at"])
                food = foodController.show_all_free({"id": data_temp["id_food"]})
                if food:
                    data_temp["food_name"] = food[0]["name"]
                    data_temp["food_image"] = food[0]["image"]
                    data_temp["category_id"] = food[0]["type_food"]
                    data_temp["category_name"] = ""
                ctn.append(data_temp)
            return ctn
        except Exception as error:
            print("Error: =>", error)
            return []
            
    def insert(self, data):
        id_food = data["id_food"]
        quantity = data["quantity"]
        observation = data["observation"]
        order_dishes_id = data["order_dishes_id"]
        type_order = data["type_order"]
        id_admin = data["id_admin"]
        prepared_data = DataOrder(
                id_food = id_food,
                quantity = quantity,
                observation = observation,
                order_dishes_id = order_dishes_id,
                type_order = type_order,
                id_admin = id_admin,
            )
        db.session.add(prepared_data)
        db.session.commit()
    
        return prepared_data
    
    def delete(self, data_filter):
        
        query = DataOrder.query
        if "id" in data_filter.keys():
            query = query.filter(DataOrder.id == data_filter["id"])
        if "order_id" in data_filter.keys():
            query = query.filter(DataOrder.order_dishes_id == data_filter["order_id"])

        fila = query.all()
        
        for j in fila:
            db.session.delete(j)
        
        db.session.commit()
        return fila
        
    
    def update(self, id, data):
        response = DataOrder.query.filter(DataOrder.id == id, DataOrder.id_admin == data["id_admin"]).first()
        del(data["id_admin"])
        
        if response:
            for key, value in data.items():
                setattr(response, key, value)
        
        db.session.commit()
        
        return response