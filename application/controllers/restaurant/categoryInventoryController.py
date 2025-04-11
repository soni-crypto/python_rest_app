from flask import current_app
from application.models.Restaurant import InventoryCategory,db
from application.helpers.gestor_restaurant import ManagerData
from application.controllers.restaurant.historyController import StockHistoryC
from sqlalchemy import desc, or_
from application.controllers.restaurant.configurationDataController import ConfigurationDataController
import pytz

managerData = ManagerData()
recordModel = StockHistoryC()
configurationDataController = ConfigurationDataController()

class InventoryCategoryController:
    app=None
    def __init__(self):
        self.app = current_app

    def get_all_free(self, d_json):
        try:
            query = InventoryCategory.query
            if "id" in d_json.keys():
                query = query.filter(InventoryCategory.id == d_json["id"])
            if "id_admin" in d_json.keys():
                query = query.filter(InventoryCategory.id_admin == d_json["id_admin"])
            if "state_order" in d_json.keys():
                if isinstance(d_json["state_order"], list):
                    query = query.filter(or_(*[InventoryCategory.state_order == state for state in d_json["state_order"]]))
                else:
                    query = query.filter(InventoryCategory.state_order == d_json["state_order"])
            if "desc" in d_json.keys():
                query = query.order_by(desc(InventoryCategory.id))

            if "limit" in d_json.keys():
                data = query.limit(d_json["limit"]).all()
            else:
                data = query.limit(50).all()

            time_zone = ""
            for d in data:
                if not time_zone:
                    dataConfigAdmin = configurationDataController.read({"id_admin":d.id_admin})[0]
                    time_zone = pytz.timezone(dataConfigAdmin.time_zone) 
                d.created_at = d.created_at.astimezone(time_zone)
                
            return data
        except Exception as error:
            print("Error: ", error)
            return []
            
    def insert(self, data):
        id_admin = data["id_admin"]
        name = data["name"]
        description = data["description"]
        state = data["state"]
        image_id = data["image_id"]
        
        prepared_data = InventoryCategory(
                id_admin = id_admin,
                name = name,
                image_id = image_id,
                state = state,
                description = description,
            )
        
        db.session.add(prepared_data)
        db.session.commit()
        return prepared_data
    
    def delete(self, data_filter):
        
        query = InventoryCategory.query
        if "id" in data_filter.keys():
            query = query.filter(InventoryCategory.id == data_filter["id"])
        if "id_admin" in data_filter.keys():
            query = query.filter(InventoryCategory.id_admin == data_filter["id_admin"])
        
        fila = query.all()
        for f in fila:
            db.session.delete(f)
        db.session.commit()
        return fila
    
    def update(self, id, data):
        response = InventoryCategory.query.filter(InventoryCategory.id == id, InventoryCategory.id_admin == data["id_admin"]).first()
        del (data["id_admin"])
        if response:
            for key, value in data.items():
                setattr(response, key, value)
        
        db.session.commit()
            
        return response            
            