from flask import current_app
from application.models.Restaurant import SalesInventory,db
from sqlalchemy import desc, or_
from application.controllers.restaurant.configurationDataController import ConfigurationDataController
import pytz
import copy
configurationDataController = ConfigurationDataController()

class SalesInventoryController:
    app=None
    def __init__(self):
        self.app = current_app

    def get_all_free(self, d_json):
        try:
            query = SalesInventory.query
            if "id" in d_json.keys():
                query = query.filter(SalesInventory.id == d_json["id"])
            if "id_admin" in d_json.keys():
                query = query.filter(SalesInventory.id_admin == d_json["id_admin"])
            if "id_product" in d_json.keys():
                query = query.filter(SalesInventory.id_product == d_json["id_product"])
            if "customer" in d_json.keys():
                query = query.filter(SalesInventory.customer == d_json["customer"])
            if "state" in d_json.keys():
                query = query.filter(SalesInventory.state == d_json["state"])
            if "date_start" in d_json.keys():
                query = query.filter(SalesInventory.created_at >= d_json["date_start"])
            if "date_end" in d_json.keys():
                query = query.filter(SalesInventory.created_at <= d_json["date_end"])
            if "desc" in d_json.keys():
                query = query.order_by(desc(SalesInventory.id))

            if "limit" in d_json.keys():
                data = query.limit(d_json["limit"]).all()
            else:
                data = query.limit(100).all()

            time_zone = ""
            data_copy = copy.deepcopy(data)
            for d in data_copy:
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
        id_product = data["id_product"]
        customer = data["customer"]
        quantity = data["quantity"]
        discount = data["discount"]
        pay_method = data["pay_method"]
        amount_unsettled = data["amount_unsettled"]
        amount_due = data["amount_due"]
        amount_paid = data["amount_paid"]
        state = data["state"]
        
        prepared_data = SalesInventory(
                id_admin = id_admin,
                id_product = id_product,
                customer = customer,
                quantity = quantity,
                discount = discount,
                pay_method = pay_method,
                amount_unsettled = amount_unsettled,
                amount_due = amount_due,
                amount_paid = amount_paid,
                state = state,
            )
        
        db.session.add(prepared_data)
        db.session.commit()
        return prepared_data
    
    def delete(self, data_filter):
        query = SalesInventory.query
        if "id" in data_filter.keys():
            query = query.filter(SalesInventory.id == data_filter["id"])
        if "id_admin" in data_filter.keys():
            query = query.filter(SalesInventory.id_admin == data_filter["id_admin"])
        
        fila = query.all()
        for f in fila:
            db.session.delete(f)
        db.session.commit()
        return fila
    
    def update(self, id, data):
        response = SalesInventory.query.filter(SalesInventory.id == id, SalesInventory.id_admin == data["id_admin"]).first()
        del(data["id_admin"])
        if response:
            for key, value in data.items():
                setattr(response, key, value)
        
        db.session.commit()
            
        return response            
            
            
            