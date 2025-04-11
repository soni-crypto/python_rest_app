from sqlalchemy import desc
from flask import current_app
from application.models.Restaurant import StockHistory, db
from application.controllers.restaurant.waitressController import WaitressMainC
from application.controllers.restaurant.userController import UsersAdmin
from application.helpers.gestor_restaurant import ManagerData
from application.controllers.restaurant.configurationDataController import ConfigurationDataController
import pytz

managerData = ManagerData()
configurationDataController = ConfigurationDataController()
usersAdmin = UsersAdmin()

class StockHistoryC:
    app = current_app
    def show_all(self):
        id_admin = managerData.email_to_id_admin()    
        dataConfigAdmin = configurationDataController.read({"id_admin":id_admin})[0]
        time_zone = pytz.timezone(dataConfigAdmin.time_zone)
        
        data_full = StockHistory.query.filter(StockHistory.id_user_admin == id_admin).all()
        for i in data_full:
            i.created_at = time_zone.localize(i.created_at)

        db.session.commit()
            
        return data_full
    
    def show_filter(self, data_json = False):
        waitressController = WaitressMainC()
        id_user_context = data_json["id_user_admin"]
        dataConfigAdmin = configurationDataController.read({"id_admin":id_user_context})[0]
        time_zone = pytz.timezone(dataConfigAdmin.time_zone) 
        
        query = StockHistory.query
        if "id_user_admin"  in data_json.keys():
            query = query.filter(StockHistory.id_user_admin == data_json["id_user_admin"])
            
        if "id_user_captured"  in data_json.keys():
            query = query.filter(StockHistory.id_user_captured== data_json["id_user_captured"])

        if "date_start" in data_json.keys():
            query = query.filter(StockHistory.created_at >= data_json["date_start"])

        if "date_end" in data_json.keys():
            query = query.filter(StockHistory.created_at <= data_json["date_end"])

        if "user_level" in data_json.keys():
            query = query.filter(StockHistory.user_level == data_json["user_level"])
        
        data_full = query.order_by(desc(StockHistory.id)).limit(150).all()
        for i in data_full:
            i.created_at = i.created_at.astimezone(time_zone)
            if i.user_level == 4:
                waitress = waitressController.show_all({"id":i.id_user_captured})
                if waitress:
                    i.user_name = waitress[0].user_first_name + ", " + waitress[0].user_last_name
                else:
                    i.user_name = "Usuario";
            elif i.user_level == 2:
                res = usersAdmin.show_all({"id_admin":i.id_user_captured})
                if res:
                    i.user_name = res[0]["user_name"]+ ", "+ res[0]["user_surnames"]
                else:
                    i.user_name = "Administrador"
            else:
                i.user_name = ""
                    
        return data_full

    def insert_record(self, *args, **kwargs):
        id_user_context_admin = managerData.email_to_id_admin()
        
        data_full = StockHistory(
            id_user_captured = managerData.email_to_id(),
            order_code = kwargs["order_code"],
            added_amount = kwargs["added_amount"],
            movement_created = kwargs["movement_created"],
            description_action = kwargs["description_action"],
            id_user_admin = id_user_context_admin,
            user_level = managerData.level_saved_cookie_or_session(),
        )
        db.session.add(data_full)
        db.session.commit()
        return data_full
    
    def update_record(self, *args, **kwargs):
        id_user_context = managerData.email_to_id_admin()
        id = kwargs["id"]
        

        row = StockHistory.query.filter(StockHistory.id == id, StockHistory.id_user_admin == id_user_context).first()
        if row:
            row.added_amount = kwargs["added_amount"]
        db.session.commit()
                            
        return row
    
    