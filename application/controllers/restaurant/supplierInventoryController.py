from flask import current_app
from application.models.Restaurant import SupplierInventory,db
from sqlalchemy import desc, or_
from application.controllers.restaurant.configurationDataController import ConfigurationDataController
import pytz
configurationDataController = ConfigurationDataController()

class SupplierInventoryController:
    app=None
    def __init__(self):
        self.app = current_app

    def get_all_free(self, d_json):
        try:
            query = SupplierInventory.query
            if "id" in d_json.keys():
                query = query.filter(SupplierInventory.id == d_json["id"])
            if "id_admin" in d_json.keys():
                query = query.filter(SupplierInventory.id_admin == d_json["id_admin"])            
            if "desc" in d_json.keys():
                query = query.order_by(desc(SupplierInventory.id))

            if "limit" in d_json.keys():
                data = query.limit(d_json["limit"]).all()
            else:
                data = query.limit(50).all()

            time_zone = ""
            for d in data:
                if not time_zone:
                    dataConfigAdmin = configurationDataController.read({"id_admin":d.id_admin})[0]
                    time_zone = pytz.timezone(dataConfigAdmin.time_zone) 
                d.created_at = d.created_at.astimezone(time_zone)
                
            return data
        except Exception as error:
            print("Error: ", error)
            return []
            
    def insert(self, data):
        id_admin = data["id_admin"]
        name = data["name"]
        company_name = data["company_name"]
        description = data["description"]
        address = data["address"]
        city = data["city"]
        country = data["country"]
        email = data["email"]
        phone = data["phone"]
        tax_id = data["tax_id"]
        bank_account_number = data["bank_account_number"]
        state = data["state"]
        
        prepared_data = SupplierInventory(
                id_admin = id_admin,
                name = name,
                description = description,
                company_name = company_name,
                address = address,
                city = city,
                country = country,
                email = email,
                phone = phone,
                tax_id = tax_id,
                bank_account_number = bank_account_number,
                state = state,
            )
        
        db.session.add(prepared_data)
        db.session.commit()
        return prepared_data
    
    def delete(self, data_filter):
        query = SupplierInventory.query
        if "id" in data_filter.keys():
            query = query.filter(SupplierInventory.id == data_filter["id"])
        if "id_admin" in data_filter.keys():
            query = query.filter(SupplierInventory.id_admin == data_filter["id_admin"])
        
        fila = query.all()
        for f in fila:
            db.session.delete(f)
        db.session.commit()
        return fila
    
    def update(self, id, data):
        response = SupplierInventory.query.filter(SupplierInventory.id == id, SupplierInventory.id_admin == data["id_admin"]).first()
        del(data["id_admin"])
        if response:
            for key, value in data.items():
                setattr(response, key, value)
        
        db.session.commit()
            
        return response            
            
            
            