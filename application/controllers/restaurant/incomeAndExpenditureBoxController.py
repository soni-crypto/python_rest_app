from flask import current_app
from application.models.Restaurant import IncomeAndExpenditureBox, db
from application.helpers.gestor_restaurant import ManagerData
from sqlalchemy import desc, or_
from application.controllers.restaurant.configurationDataController import ConfigurationDataController
import pytz
from datetime import datetime
import copy
managerData = ManagerData()
configurationDataController = ConfigurationDataController()

class IncomeAndExpenditureBoxController:
    app=None
    def __init__(self):
        self.app = current_app

    def read(self, d_json):
        try:
            query = IncomeAndExpenditureBox.query
            if "id" in d_json.keys():
                query = query.filter(IncomeAndExpenditureBox.id == d_json["id"])
            if "id_admin" in d_json.keys():
                query = query.filter(IncomeAndExpenditureBox.id_admin == d_json["id_admin"])
            if "state" in d_json.keys():
                query = query.filter(IncomeAndExpenditureBox.state == d_json["state"])
            if "limit" in d_json.keys():
                data = query.limit(d_json["limit"]).all()
            else:
                data = query.limit(50).all()
            
            return data
        
        except Exception as error:
            print("Error: ", error)
            return []
            
    def insert(self, data):
        id_admin = data["id_admin"]
        motive = data["motive"]
        amount = data["amount"]
        type = data["type"]
        amt = data["amt"]
        state = 1

        prepared_data = IncomeAndExpenditureBox(
                id_admin = id_admin,
                motive = motive,
                amount = amount,
                type = type,
                amt = amt,
                state = state,
            )
        
        db.session.add(prepared_data)
        db.session.commit()
        return prepared_data
    
    def delete(self, data_filter):
        query = IncomeAndExpenditureBox.query
        if "id" in data_filter.keys():
            query = query.filter(IncomeAndExpenditureBox.id == data_filter["id"])
        if "id_admin" in data_filter.keys():
            query = query.filter(IncomeAndExpenditureBox.id_admin == data_filter["id_admin"])
        
        fila = query.all()
        for f in fila:
            db.session.delete(f)
        db.session.commit()
        return fila
    
    def update(self, id, data):
        response = IncomeAndExpenditureBox.query.filter(IncomeAndExpenditureBox.id == id, IncomeAndExpenditureBox.id_admin == data["id_admin"]).first()
        del(data["id_admin"])
        if response:
            for key, value in data.items():
                setattr(response, key, value)
        
        db.session.commit()
        return response            
            