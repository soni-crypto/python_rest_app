from flask import current_app
from application.models.Restaurant import AvailabilityCalendar, db
from application.helpers.gestor_restaurant import ManagerData
from sqlalchemy import desc, or_
from application.controllers.restaurant.configurationDataController import ConfigurationDataController
import pytz
from datetime import datetime
import copy
managerData = ManagerData()
configurationDataController = ConfigurationDataController()

class AvailabilityCalendarController:
    app=None
    def __init__(self):
        self.app = current_app

    def read(self, d_json):
        try:
            query = AvailabilityCalendar.query
            if "id" in d_json.keys():
                query = query.filter(AvailabilityCalendar.id == d_json["id"])
            if "id_admin" in d_json.keys():
                query = query.filter(AvailabilityCalendar.id_admin == d_json["id_admin"])
            
            data = query.all()
            
            return data
        
        except Exception as error:
            print("Error: ", error)
            return []
            
    def insert(self, data):
        id_admin            = data["id_admin"]
        title               = data["title"]
        start               = data["start"]
        end                 = data["end"]
        color               = data["color"]
        backgroundColor     = data["backgroundColor"]
        textColor           = data["textColor"]
        borderColor         = data["borderColor"]
        display             = data["display"]
        overlap             = data["overlap"]
        groupId             = data["groupId"]
        constraint          = data["constraint"]
        state               = data["state"]
        # 

        prepared_data = AvailabilityCalendar(
                id_admin        = id_admin  ,
                title           = title     ,
                start           = start     ,
                end             = end       ,
                color           = color     ,
                backgroundColor = backgroundColor,
                textColor       = textColor,
                borderColor     = borderColor,
                display         = display   ,
                overlap         = overlap   ,
                groupId         = groupId   ,
                constraint      = constraint,
                state           = state,
            )
        
        db.session.add(prepared_data)
        db.session.commit()
        return prepared_data
    
    def delete(self, data_filter):
        query = AvailabilityCalendar.query
        if "id" in data_filter.keys():
            query = query.filter(AvailabilityCalendar.id == data_filter["id"])
        if "id_admin" in data_filter.keys():
            query = query.filter(AvailabilityCalendar.id_admin == data_filter["id_admin"])
        
        fila = query.all()
        for f in fila:
            db.session.delete(f)
        db.session.commit()
        return fila
    
    def update(self, id, data):
        response = AvailabilityCalendar.query.filter(AvailabilityCalendar.id == id, AvailabilityCalendar.id_admin == data["id_admin"]).first()
        del(data["id_admin"])
        if response:
            for key, value in data.items():
                setattr(response, key, value)
        
        db.session.commit()
        return response            
            