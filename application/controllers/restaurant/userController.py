from flask import current_app
from fuzzywuzzy import fuzz
from application.models.Restaurant import User, db
from application.controllers.restaurant.availableCountries import availableCountries
import copy
class UsersAdmin():
    app = current_app
    
    def read_admins_percentage (self, data_for_filter={}):
        profiles = []
        data = User.query.all()
        data_counter = 0
        for i in data:
            percent = fuzz.ratio(data_for_filter["id_secondary"], i.id_secondary)
            
            if percent >= 70:
                data_admin = {
                    "user_number" : i.user_number,
                    "id_secondary" : i.id_secondary,
                    "company_name" : i.company_name,
                    "company_description" : i.company_description,
                    "company_icon" : i.company_icon,
                    "company_image" : i.company_image,
                    "user_email" : i.user_email,
                    "company_location_1" : i.company_location_1,
                    "company_location_2" : i.company_location_2,
                }
                profiles.append(data_admin)
                data_counter += 1
                if data_counter == 9:
                    break
                
        return profiles
    
    def show_all(self, data_for_filter={}):
        ctn=[]
    
        query = User.query
        if "id_secondary" in data_for_filter.keys():
            query = query.filter(User.id_secondary == data_for_filter["id_secondary"])
        if "id_admin" in data_for_filter.keys():
            query = query.filter(User.id == data_for_filter["id_admin"])
        
        data = query.all()
        if data:
            for i in data:
                data_prepared = i.__dict__
                del(data_prepared["_sa_instance_state"])
                del(data_prepared["user_password"])
                if (data_prepared["company_location_1"]):
                    avC = availableCountries()
                    resp_avC = avC.get_everything({"id":data_prepared["company_location_1"]})
                    if resp_avC:
                        data_prepared["company_location_1"] = resp_avC[0]["country_name"]
                ctn.append(data_prepared)
            
        return ctn
    
    def show_id(self, id_):
        ctn = {}
        with self.app.app_context():
            data = User.query.filter(User.id == id_).first()
            if data:
                ctn = data.__dict__
                del(ctn["_sa_instance_state"])
                del(ctn["user_password"])
                
        db.session.commit()        
        return ctn
    
    def validate_user(self, email, password):
        
        with self.app.app_context():
            row_search = User.query.filter(User.user_email == email , User.user_password == password).first()
            if row_search:
                return row_search.id
            else:
                return False
            
    def insert_user(self, *args, **kwargs):
        data = User(
            subscription_end_date = kwargs["subscription_end_date"],
            user_name = kwargs["user_name"],
            user_surnames = kwargs["user_surnames"],
            user_email = kwargs["user_email"],
            user_number = kwargs["user_number"],
            user_password = kwargs["user_password"],
            user_image = kwargs["user_image"],
            user_type = 2,
            user_key_room_app = kwargs["user_key_room_app"],
        )
        db.session.add(data)
        db.session.commit() 
        return data
    
    def user_update(self, id, data):
        response = User.query.filter(User.id == id).first()
        if response:
            for key, value in data.items():
                setattr(response, key, value)
            db.session.commit()
            
        return response