from flask import current_app
from application.models.Restaurant import Inventory,db
from application.helpers.gestor_restaurant import ManagerData
from application.controllers.restaurant.historyController import StockHistoryC
from sqlalchemy import desc, or_
from application.controllers.restaurant.configurationDataController import ConfigurationDataController
import pytz
from datetime import datetime
import copy
managerData = ManagerData()
recordModel = StockHistoryC()
configurationDataController = ConfigurationDataController()

class InventoryController:
    app=None
    def __init__(self):
        self.app = current_app

    def get_all_free(self, d_json):
        try:
            query = Inventory.query
            if "id" in d_json.keys():
                query = query.filter(Inventory.id == d_json["id"])
            if "id_admin" in d_json.keys():
                query = query.filter(Inventory.id_admin == d_json["id_admin"])
            if "product_code" in d_json.keys():
                query = query.filter(Inventory.product_code == d_json["product_code"])
            if "inventory_category_id" in d_json.keys():
                query = query.filter(Inventory.inventory_category_id == d_json["inventory_category_id"])
            if "expiration_date_start" in d_json.keys():
                query = query.filter(Inventory.expiration_date >= d_json["expiration_date_start"])
            if "expiration_date_end" in d_json.keys():
                query = query.filter(Inventory.expiration_date <= d_json["expiration_date_end"])
            if "state_order" in d_json.keys():
                if isinstance(d_json["state_order"], list):
                    query = query.filter(or_(*[Inventory.state_order == state for state in d_json["state_order"]]))
                else:
                    query = query.filter(Inventory.state_order == d_json["state_order"])
            if "desc" in d_json.keys():
                query = query.order_by(desc(Inventory.id))

            if "limit" in d_json.keys():
                data = query.limit(d_json["limit"]).all()
            else:
                data = query.limit(50).all()
            
            time_zone = ""
            data_copy = copy.deepcopy(data)
            for d in data_copy:
                if not time_zone:
                    dataConfigAdmin = configurationDataController.read({"id_admin":d.id_admin})[0]
                    time_zone = pytz.timezone(dataConfigAdmin.time_zone) 
                d.created_at = d.created_at.astimezone(time_zone)
                d.expiration_date = datetime.strptime(d.expiration_date, "%Y-%m-%d")
                d.expiration_date = d.expiration_date.strftime("%d-%m-%Y")
            return data
        except Exception as error:
            print("Error: ", error)
            return []
            
    def insert(self, data):
        id_admin = data["id_admin"]
        category_id = data["category_id"]
        name = data["name"]
        description = data["description"]
        quantity = data["quantity"]
        purchase_price = data["purchase_price"]
        sale_price = data["sale_price"]
        unit_of_measurement = data["unit_of_measurement"]
        expiration_date = data["expiration_date"]
        image_id = data["image_id"]
        state = data["state"]
        
        prepared_data = Inventory(
                id_admin = id_admin,
                inventory_category_id = category_id,
                name = name,
                description = description,
                quantity = quantity,
                purchase_price = purchase_price,
                sale_price = sale_price,
                unit_of_measurement = unit_of_measurement,
                expiration_date = expiration_date,
                image_id = image_id,
                state = state,
            )
        
        db.session.add(prepared_data)
        db.session.commit()
        return prepared_data
    
    def delete(self, data_filter):
        query = Inventory.query
        if "id" in data_filter.keys():
            query = query.filter(Inventory.id == data_filter["id"])
        if "id_admin" in data_filter.keys():
            query = query.filter(Inventory.id_admin == data_filter["id_admin"])
        if "category_id" in data_filter.keys():
            query = query.filter(Inventory.inventory_category_id == data_filter["category_id"])
        
        fila = query.all()
        for f in fila:
            db.session.delete(f)
        db.session.commit()
        return fila
    
    def update(self, id, data):
        response = Inventory.query.filter(Inventory.id == id, Inventory.id_admin == data["id_admin"]).first()
        del(data["id_admin"])
        if response:
            for key, value in data.items():
                setattr(response, key, value)
        
        db.session.commit()
        return response            
            
            
            