from flask import current_app
from application.helpers.gestor_restaurant import ManagerData
from application.controllers.restaurant.userController import UsersAdmin
from application.models.Restaurant import db, ConfigurationData

from sqlalchemy import desc
import datetime
import json

managerData = ManagerData()
adminsController = UsersAdmin()
class ConfigurationDataController:
    app=None
    def __init__(self):
        self.app = current_app

    def read(self, d_json):
        try:
            query = ConfigurationData.query
            if "id" in d_json.keys():
                query = query.filter(ConfigurationData.id == d_json["id"])
            if "id_admin" in d_json.keys():
                query = query.filter(ConfigurationData.id_admin == d_json["id_admin"])

            data = query.all()
            return data
        
        except Exception as error:
            print("Error: ", error)
            return []
            
    def insert(self, data):
        id_admin = data["id_admin"]
        # email = data["email"]
        # password_email = data["password_email"]
        # language = data["language"]
        # currency = data["currency"]
        time_zone = data["time_zone"]
        # order_now = data["order_now"]
        # reservations_accept = data["reservations_accept"]
        # delivery_accept = data["delivery_accept"]
        # visibility_in_app = data["visibility_in_app"]
        # send_email_1 = data["send_email_1"]
        # send_email_2 = data["send_email_2"]
        
        prepared_data = ConfigurationData(
                id_admin = id_admin,
                # email = email,
                # password_email = password_email,
                # language = language,
                # currency = currency,
                time_zone = time_zone,
                # order_now = order_now,
                # reservations_accept = reservations_accept,
                # delivery_accept = delivery_accept,
                # visibility_in_app = visibility_in_app,
                # send_email_1 = send_email_1,
                # send_email_2 = send_email_2,    
            )
        
        db.session.add(prepared_data)
        db.session.commit()
        return prepared_data
    
    def delete(self, id):
        id_admin = managerData.email_to_id_admin()
        with self.app.app_context():
            fila = ConfigurationData.query.filter(ConfigurationData.id == id, ConfigurationData.id_admin==id_admin).first()
            
            if fila != None:
                db.session.delete(fila)
                db.session.commit()
                return {"state":200}
        
        return {"state":"User not found"}
    
    def update(self, data):
        id_admin = managerData.email_to_id_admin()
        with self.app.app_context():
            response = ConfigurationData.query.filter(ConfigurationData.id_admin == id_admin).first()
            
            if response:
                for key, value in data.items():
                    setattr(response, key, value)
            
            db.session.commit()
            
        return {"status":200}
    
                
            
            
            