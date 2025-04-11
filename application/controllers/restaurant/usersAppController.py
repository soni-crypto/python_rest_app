from flask import current_app
from application.models.Restaurant import UserApp, db
from application.helpers.gestor_restaurant import ManagerData
managerData = ManagerData()
class UsersAppController():
    app = current_app
    
    
    def read(self, data_for_filter={}):
        data = []
        query = UserApp.query
        if "id" in data_for_filter.keys():
            query = query.filter(UserApp.id == data_for_filter["id"])

        response = query.all()
        if response:
            for info in response:
                data_prepared =  info.__dict__
                del(data_prepared["_sa_instance_state"]) 
                data.append(data_prepared)
        return data
    
    def validate(self, email, tel_whats):
        data_email = UserApp.query.filter(UserApp.email == email).all()
        if data_email:
            return "email"
        data_tel_whats = UserApp.query.filter(UserApp.tel_whats == tel_whats).all()
        if data_tel_whats:
            return "tel_whats"
        
        return "ok"
    
    def login_user(self, email = False, number = False, password=False):
        query = UserApp.query
        if email:
            query = query.filter(UserApp.email == email, UserApp.password == password)
        elif number:
            query = query.filter(UserApp.tel_whats == number, UserApp.password == password)
        else:
            return False
        response = query.first()
        
        if response:
            return response
        else:
            return False
            
    def create(self, data = {}):
        data_search = UserApp.query.filter(UserApp.email == data["email"], UserApp.tel_whats == data["tel_whats"]).all()
        if data_search:
            return False
        else:
            data_prepared = UserApp(
                first_name = data["first_name"],
                last_name = data["last_name"],
                email = data["email"],
                tel_whats = data["tel_whats"],
                password = data["password"],
                image = data["image"],
            )
            db.session.add(data_prepared)
            db.session.commit()
            new_id = data_prepared.id

            return new_id
    
    def update(self, id, data):
        response = UserApp.query.filter(UserApp.id == id).first()    
        if response and data:
            for key, value in data.items():
                setattr(response, key, value)
            db.session.commit()

            return True
        else:
            return False