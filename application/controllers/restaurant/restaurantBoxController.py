from flask import current_app
from application.models.Restaurant import RestaurantBox, db
from application.helpers.gestor_restaurant import ManagerData
managerData = ManagerData()

class RestaurantBoxController():
    app = current_app
    
    def get_all(self, data_for_filter={}):
        data = []
        query = RestaurantBox.query
        if "id" in data_for_filter.keys():
            query = query.filter(RestaurantBox.id == data_for_filter["id"])
        if "id_admin" in data_for_filter.keys():
            query = query.filter(RestaurantBox.id_admin == data_for_filter["id_admin"])
        if "id_user" in data_for_filter.keys():
            query = query.filter(RestaurantBox.id_user == data_for_filter["id_user"])
        
        response = query.all()
        if response:
            for info in response:
                data_prepared =  info.__dict__
                del(data_prepared["_sa_instance_state"]) 
                data.append(data_prepared)
        return data
    
    def create(self, data = {}):
        
        if data:
            data_prepared = RestaurantBox(
                id_admin = data["id_admin"],
                id_user = data["id_user"],
                total_amount_order = data["total_amount_order"],
                daily_amount_order = data["daily_amount_order"],
                total_amount_reservation = data["total_amount_reservation"],
                daily_amount_reservation = data["daily_amount_reservation"],
                state = data["state"],
            )
            db.session.add(data_prepared)
            db.session.commit()
            return data_prepared
    
    def update(self, id, data):
        query = RestaurantBox.query
        if "id_admin" in data.keys():
            query = query.filter(RestaurantBox.id_admin == data["id_admin"])
            del(data["id_admin"])
        if id:
            query = query.filter(RestaurantBox.id == id)
        response = query.first()
        if response and data:
            for key, value in data.items():
                setattr(response, key, value)
            db.session.commit()

            return True
        else:
            return False
        
    def delete(self, id):
        response = RestaurantBox.query.filter(RestaurantBox.id == id).first()    
        if response:
            db.session.delete(response)
            db.session.commit()

            return True
        else:
            return False