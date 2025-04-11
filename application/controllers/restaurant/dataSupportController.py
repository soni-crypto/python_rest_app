from flask import current_app
from application.models.Restaurant import DataSupport, db
from application.helpers.gestor_restaurant import ManagerData
managerData = ManagerData()

class DataSupportController():
    app = current_app
    
    
    def get_all(self, data_for_filter={}):
        data = []
        query = DataSupport.query
        if "id" in data_for_filter.keys():
            query = query.filter(DataSupport.id == data_for_filter["id"])
        if "id_user" in data_for_filter.keys():
            query = query.filter(DataSupport.id == data_for_filter["id_user"])
        if "email" in data_for_filter.keys():
            query = query.filter(DataSupport.id == data_for_filter["email"])
        
        response = query.all()
        if response:
            for info in response:
                data_prepared =  info.__dict__
                del(data_prepared["_sa_instance_state"]) 
                data.append(data_prepared)
        return data
    
    def create(self, data = {}):
        with self.app.app_context():
            if data:
                data_prepared = DataSupport(
                    id_user = data["id_user"],
                    level_user = data["level_user"],
                    email = data["email"],
                    message = data["message"],
                    files = data["files"],
                    state = data["state"],
                )
                db.session.add(data_prepared)
                db.session.commit()
                new_id = data_prepared.id

                return new_id
    
    def update(self, id, data):
        response = DataSupport.query.filter(DataSupport.id == id).first()    
        if response and data:
            for key, value in data.items():
                setattr(response, key, value)
            db.session.commit()

            return True
        else:
            return False
        
    def delete(self, id):
        response = DataSupport.query.filter(DataSupport.id == id).first()    
        if response:
            db.session.delete(response)
            db.session.commit()

            return True
        else:
            return False