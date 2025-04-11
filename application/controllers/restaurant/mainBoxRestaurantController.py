from flask import current_app
from application.models.Restaurant import MainBoxRestaurant, db
from application.helpers.gestor_restaurant import ManagerData
from sqlalchemy import desc, or_
from application.controllers.restaurant.configurationDataController import ConfigurationDataController
import pytz
from datetime import datetime
import copy
managerData = ManagerData()
configurationDataController = ConfigurationDataController()

class MainBoxRestaurantController:
    app=None
    def __init__(self):
        self.app = current_app

    def read(self, d_json):
        try:
            query = MainBoxRestaurant.query
            if "id" in d_json.keys():
                query = query.filter(MainBoxRestaurant.id == d_json["id"])
            if "id_admin" in d_json.keys():
                query = query.filter(MainBoxRestaurant.id_admin == d_json["id_admin"])
            if "box_status" in d_json.keys():
                query = query.filter(MainBoxRestaurant.box_status == d_json["box_status"])
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
            return data_copy
        
        except Exception as error:
            print("Error: ", error)
            return []
            
    def insert(self, data):
        id_admin = data["id_admin"]
        box_name = data["box_name"]
        initial_amount = data["initial_amount"]
        current_amount = data["current_amount"]
        opened_by_id = data["opened_by_id"]
        closed_by_id = data["closed_by_id"]
        opened_by_level = data["opened_by_id"]
        closed_by_level = data["closed_by_id"]
        box_status = 0

        prepared_data = MainBoxRestaurant(
                id_admin = id_admin,
                box_name = box_name,
                initial_amount = initial_amount,
                current_amount = current_amount,
                opened_by_id = opened_by_id,
                closed_by_id = closed_by_id,
                opened_by_level = opened_by_level,
                closed_by_level = closed_by_level,
                box_status  = box_status,
            )
        
        db.session.add(prepared_data)
        db.session.commit()
        return prepared_data
    
    def delete(self, data_filter):
        query = MainBoxRestaurant.query
        if "id" in data_filter.keys():
            query = query.filter(MainBoxRestaurant.id == data_filter["id"])
        if "id_admin" in data_filter.keys():
            query = query.filter(MainBoxRestaurant.id_admin == data_filter["id_admin"])
        
        fila = query.all()
        for f in fila:
            db.session.delete(f)
        db.session.commit()
        return fila
    
    def update(self, id_admin, data):
        response = MainBoxRestaurant.query.filter(MainBoxRestaurant.id_admin == id_admin).first()
        if response:
            for key, value in data.items():
                setattr(response, key, value)
        
        db.session.commit()
        return response            
            