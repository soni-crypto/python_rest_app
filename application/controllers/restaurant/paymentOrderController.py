from flask import current_app
from application.models.Restaurant import PaymentOrder, db
from application.helpers.gestor_restaurant import ManagerData
from sqlalchemy import desc, or_
from application.controllers.restaurant.configurationDataController import ConfigurationDataController
import pytz
from datetime import datetime
import copy
managerData = ManagerData()
configurationDataController = ConfigurationDataController()

class PaymentOrderController:
    app=None
    def __init__(self):
        self.app = current_app

    def read(self, d_json):
        try:
            query = PaymentOrder.query
            if "id" in d_json.keys():
                query = query.filter(PaymentOrder.id == d_json["id"])
            if "id_admin" in d_json.keys():
                query = query.filter(PaymentOrder.id_admin == d_json["id_admin"])
            if "date_start" in d_json.keys():
                query = query.filter(PaymentOrder.created_at >= d_json["date_start"])
            if "date_end" in d_json.keys():
                query = query.filter(PaymentOrder.created_at <= d_json["date_end"])
            if "state" in d_json.keys():
                if isinstance(d_json["state"], list):
                    query = query.filter(or_(*[PaymentOrder.state_order == state for state in d_json["state"]]))
                else:
                    query = query.filter(PaymentOrder.state == d_json["state"])
            if "desc" in d_json.keys():
                query = query.order_by(desc(PaymentOrder.id))

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
                
            return data
        except Exception as error:
            print("Error: ", error)
            return []
            
    def insert(self, data):
        id_admin = data["id_admin"]
        amt_1 = data["amt_1"]
        amt_2 = data["amt_2"]
        amt_3 = data["amt_3"]
        amt_4 = data["amt_4"]
        amt_5 = data["amt_5"]
        amt_6 = data["amt_6"]
        state = 1
        order_or_table_id = data["order_or_table_id"]
        mode = data["mode"]
        prepared_data = PaymentOrder(
                id_admin = id_admin,
                amt_1 = amt_1,
                amt_2 = amt_2,
                amt_3 = amt_3,
                amt_4 = amt_4,
                amt_5 = amt_5,
                amt_6 = amt_6,
                state = state,
                order_or_table_id = order_or_table_id,
                mode = mode,
            )
        
        db.session.add(prepared_data)
        db.session.commit()
        return prepared_data
    
    def delete(self, data_filter):
        query = PaymentOrder.query
        if "id" in data_filter.keys():
            query = query.filter(PaymentOrder.id == data_filter["id"])
        if "id_admin" in data_filter.keys():
            query = query.filter(PaymentOrder.id_admin == data_filter["id_admin"])
        
        fila = query.all()
        for f in fila:
            db.session.delete(f)
        db.session.commit()
        return fila
    
    def update(self, id, data):
        response = PaymentOrder.query.filter(PaymentOrder.id == id, PaymentOrder.id_admin == data["id_admin"]).first()
        del(data["id_admin"])
        if response:
            for key, value in data.items():
                setattr(response, key, value)
        
        db.session.commit()
        return response            
            
            
            