from flask import current_app
from application.models.Restaurant import Table, db
from application.helpers.gestor_restaurant import ManagerData
from application.controllers.restaurant.userController import UsersAdmin
from application.controllers.restaurant.tableCategoryController import TableCategoryController
from sqlalchemy import desc

managerData = ManagerData()
adminsController = UsersAdmin()
tableCategoryController = TableCategoryController()
class TableController:
    app=None
    def __init__(self):
        self.app = current_app

    def read(self, d_json):
        try:
            query = Table.query
            if "id" in d_json.keys():
                query = query.filter(Table.id == d_json["id"])
            if "number_table" in d_json.keys():
                query = query.filter(Table.number_table == d_json["number_table"])
            if "id_admin" in d_json.keys():
                query = query.filter(Table.id_admin == d_json["id_admin"])
            if "state" in d_json.keys():
                query = query.filter(Table.state == d_json["state"])
            if "id_user_app" in d_json.keys():
                query = query.filter(Table.id_user_app == d_json["id_user_app"])
            if "category_id" in d_json.keys():
                query = query.filter(Table.category_id == d_json["category_id"])

            data = query.order_by(Table.number_table).all()
            for d in data:
                r = tableCategoryController.read({"id":d.category_id})
                if r:
                    d.category_name = r[0].name
            return data
        except Exception as error:
            print("Error: ", error)
            return []
            
    def insert(self, data):
        id_admin = data["id_admin"]
        number_table = data["number_table"]
        state = data["state"]
        limit_number_of_users = data["limit_number_of_users"]
        category_id = data["category_id"]
        prepared_data = Table(
                id_admin = id_admin,
                number_table = number_table,
                state = state,
                limit_number_of_users = limit_number_of_users,
                category_id = category_id,
            )
        db.session.add(prepared_data)
        db.session.commit()
    
        return prepared_data
    
    def delete(self, id):
        id_admin = managerData.email_to_id_admin()
    
        fila = Table.query.filter(Table.id == id, Table.id_admin==id_admin).first()
        
        if fila != None:
            db.session.delete(fila)
            db.session.commit()
            return {"state":200}
    
        return fila
    
    def update(self, id, data):
        response = Table.query.filter(Table.id == id, Table.id_admin == data["id_admin"]).first()
        del(data["id_admin"])
        if response:
            for key, value in data.items():
                setattr(response, key, value)
        
        db.session.commit()
        
        return response