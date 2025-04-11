from sqlalchemy import desc, or_
from flask import current_app
from application.models.Restaurant import CommentsFood, db
from application.helpers.gestor_restaurant import ManagerData
from application.controllers.restaurant.configurationDataController import ConfigurationDataController
import pytz

managerData = ManagerData()
configurationDataController = ConfigurationDataController()

class CommentsFoodController:
    app = current_app
    def get_everything(self, data_query={}):
        dataConfigAdmin = configurationDataController.read({"id_admin":data_query["id_admin"]})[0]
        time_zone = pytz.timezone(dataConfigAdmin.time_zone) 
        ctn=[]
        with self.app.app_context():
            query = CommentsFood.query
            if "id" in data_query.keys():
                query = query.filter(CommentsFood.id == data_query["id"])
            if "id_admin" in data_query.keys():
                query = query.filter(CommentsFood.id_admin == data_query["id_admin"])
            if "id_type_food" in data_query.keys():
                query = query.filter(or_(CommentsFood.id_type_food == data_query["id_type_food"], CommentsFood.id_type_food == 0) )
            
            data = query.order_by(desc(CommentsFood.id)).all()
            for i in data:
                i.created_at = i.created_at.astimezone(time_zone)
                ctn.append({
                        "id" : i.id, 
                        "created_at" : i.created_at, 
                        "order_num" : i.order_num, 
                        "id_admin" : i.id_admin,
                        "id_type_food" : i.id_type_food, 
                        "comment_text" : i.comment_text,
                    })
            db.session.commit()
        return ctn
    
    def delete(self, id):
        try:
            id_user_context = managerData.email_to_id_admin()
            with self.app.app_context():
                row = CommentsFood.query.filter(CommentsFood.id == id, CommentsFood.id_admin == id_user_context).first()
                if row:
                    db.session.delete(row)
                    db.session.commit()
            return "ok"
        except Exception as err:
            return "error"
        
    def update(self, id, data):
        id_user_context = managerData.email_to_id_admin()
        with self.app.app_context():
            row = CommentsFood.query.filter(CommentsFood.id == id, CommentsFood.id_admin == id_user_context).first()
            if row:
                # Actualiza todos los campos con los valores proporcionados en 'data'
                for key, value in data.items():
                    setattr(row, key, value)
                db.session.commit()
                return "ok"
            else:
                return "no hay datos"
    
    def insert(self, data=False):
        id_user_context = managerData.email_to_id_admin()
        if (id_user_context == 0):
            return "not_linked"
        else:
            with self.app.app_context():
                data_full = CommentsFood(
                    id_admin = data["id_admin"],
                    id_type_food = data["id_type_food"],
                    comment_text = data["comment_text"],
                )
                db.session.add(data_full)
                db.session.commit()
            return "ok"