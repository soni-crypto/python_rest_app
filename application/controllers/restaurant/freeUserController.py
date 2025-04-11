from flask import current_app
from application.models.Restaurant import FreeUser, db
from application.helpers.gestor_restaurant import ManagerData
from sqlalchemy import desc, or_
from application.controllers.restaurant.configurationDataController import ConfigurationDataController
import pytz
from datetime import datetime
import copy
managerData = ManagerData()
configurationDataController = ConfigurationDataController()

class FreeUserController:
    app=None
    def __init__(self):
        self.app = current_app

    def read(self, d_json):
        try:
            query = FreeUser.query
            if "id" in d_json.keys():
                query = query.filter(FreeUser.id == d_json["id"])
            if "id_admin" in d_json.keys():
                query = query.filter(FreeUser.id_admin == d_json["id_admin"])
            if "email" in d_json.keys():
                query = query.filter(FreeUser.email == d_json["email"])
            if "limit" in d_json.keys():
                data = query.limit(d_json["limit"]).all()
            else:
                data = query.limit(50).all()
            
            
            return data
        
        except Exception as error:
            print("Error: ", error)
            return []
            
    def insert(self, data):
        id_admin = data["id_admin"]
        user_level = data["user_level"]
        name = data["name"]
        phone_number = data["phone_number"]
        email = data["email"]
        address = data["address"]

        prepared_data = FreeUser(
                id_admin = id_admin,
                user_level = user_level,
                name = name,
                phone_number = phone_number,
                email = email,
                address = address,
            )
        
        db.session.add(prepared_data)
        db.session.commit()
        return prepared_data
    
    def delete(self, data_filter):
        query = FreeUser.query
        if "id" in data_filter.keys():
            query = query.filter(FreeUser.id == data_filter["id"])
        if "id_admin" in data_filter.keys():
            query = query.filter(FreeUser.id_admin == data_filter["id_admin"])
        
        fila = query.all()
        for f in fila:
            db.session.delete(f)
        db.session.commit()
        return fila
    
    def update(self, id, data):
        response = FreeUser.query.filter(FreeUser.id == id, FreeUser.id_admin == data["id_admin"]).first()
        del(data["id_admin"])
        if response:
            for key, value in data.items():
                setattr(response, key, value)
        
        db.session.commit()
        return response            
            
            
            