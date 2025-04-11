import datetime
import json
from flask import current_app
from application.helpers.gestor_restaurant import ManagerData
from application.models.Restaurant import ReservationsFoods, db
from sqlalchemy import desc
from application.controllers.restaurant.configurationDataController import ConfigurationDataController
import pytz

managerData = ManagerData()
configurationDataController = ConfigurationDataController()

class ReservationsFoodsController:
    app = current_app
    
    def get_all(self, data_query):
        query = ReservationsFoods.query
        if "id" in data_query.keys():
            query = query.filter(ReservationsFoods.id == data_query["id"])
        if "id_admin" in data_query.keys():
            query = query.filter(ReservationsFoods.id_admin == data_query["id_admin"])
        if "id_user" in data_query.keys():
            query = query.filter(ReservationsFoods.id_user == data_query["id_user"])
        if "no_state" in data_query.keys():
            query = query.filter(ReservationsFoods.state_reservation != data_query["no_state"])
        if "only_state" in data_query.keys():
            query = query.filter(ReservationsFoods.state_reservation == data_query["only_state"])
        if "reservation_code" in data_query.keys():
            query = query.filter(ReservationsFoods.reservation_code == data_query["reservation_code"])
        
        if "limit" in data_query.keys():
            response = query.order_by(desc(ReservationsFoods.id)).limit(data_query["limit"]).all()
        else:
            response = query.order_by(desc(ReservationsFoods.id)).all()

        data_dict = []        
        id_admin_temp = 0 
        for r in response:
            if r.id_admin != id_admin_temp:
                id_admin_temp = r.id_admin
            dataConfigAdmin = configurationDataController.read({"id_admin":id_admin_temp})[0]
            time_zone = pytz.timezone(dataConfigAdmin.time_zone) 
            r.created_at = r.created_at.astimezone(time_zone)
            
            dict_prepared = r.__dict__
            del(dict_prepared["_sa_instance_state"])
            data_dict.append(dict_prepared)
        return data_dict
    
    def create_booking(self, data = False):
        with self.app.app_context():
            if data:
                prepared_data = ReservationsFoods(
                    reservation_code = data["reservation_code"],
                    id_admin = data["id_admin"],
                    id_user = data["id_user"],
                    date_reservation = data["date_reservation"],
                    time_reservation = data["time_reservation"],
                    type_reservation = data["type_reservation"],
                    message_reservation = data["message_reservation"],
                    foods_reservation = data["foods_reservation"],
                    vouchers_reservations = data["vouchers_reservations"],
                    conversation_reservation = data["conversation_reservation"],
                    user_coordinates = data["user_coordinates"],
                    price_per_delivery = data["price_per_delivery"],
                )
                db.session.add(prepared_data)
                db.session.commit() 

                return prepared_data.id
            
    def update_booking(self, data_query, data_body):
        with self.app.app_context():
            row = ReservationsFoods.query.filter(ReservationsFoods.id == data_query["id_reservation"]).first()
            if row:
                for key, value in data_body.items():
                    setattr(row, key, value )
            db.session.commit()

        return "ok"
    
    def delete_booking(self, data_filter = {}):
        with self.app.app_context():
            if data_filter:
                query = ReservationsFoods.query
                if "max_date" in data_filter and "password" in data_filter:
                    if (data_filter["password"]=="pass123fuck"):
                        query = query.filter(ReservationsFoods.date_reservation <= data_filter["max_date"])
                    else:
                        return False
                if "id" in data_filter:
                    query = query.filter(ReservationsFoods.id == data_filter["id"], ReservationsFoods.id_admin == data_filter["id_admin"])
                rows = query.all()
                for row in rows:
                    db.session.delete(row)
                    db.session.commit()
            return "ok"