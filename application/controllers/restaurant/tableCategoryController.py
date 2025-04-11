from flask import current_app
from application.models.Restaurant import TableCategory, db
from application.helpers.gestor_restaurant import ManagerData
from application.controllers.restaurant.userController import UsersAdmin
from sqlalchemy import desc

managerData = ManagerData()
adminsController = UsersAdmin()

class TableCategoryController:
    app=None
    def __init__(self):
        self.app = current_app

    def read(self, d_json):
        try:
            query = TableCategory.query
            if "id" in d_json.keys():
                query = query.filter(TableCategory.id == d_json["id"])

            if "id_admin" in d_json.keys():
                query = query.filter(TableCategory.id_admin == d_json["id_admin"])

            data = query.order_by(TableCategory.id).all()

            return data
        except Exception as error:
            print("Error: ", error)
            return []
            
    def insert(self, data):
        id_admin = data["id_admin"]
        name = data["name"]
        
        prepared_data = TableCategory(
                id_admin = id_admin,
                name = name,
                state = 1,
            )
        db.session.add(prepared_data)
        db.session.commit()
    
        return prepared_data
    
    def delete(self, data_filter):
        
        query = TableCategory.query
        if "id" in data_filter.keys():
            query = query.filter(TableCategory.id == data_filter["id"])
        if "id_admin" in data_filter.keys():
            query = query.filter(TableCategory.id_admin == data_filter["id_admin"])

        fila = query.all()
        
        for j in fila:
            db.session.delete(j)
        
        db.session.commit()
        return fila
        
    
    def update(self, id, data):
        id_admin = managerData.email_to_id_admin()
        response = TableCategory.query.filter(TableCategory.id == id, TableCategory.id_admin == id_admin).first()
        
        if response:
            for key, value in data.items():
                setattr(response, key, value)
        
        db.session.commit()
        
        return response