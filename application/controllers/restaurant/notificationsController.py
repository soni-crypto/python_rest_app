from flask import current_app
from sqlalchemy import desc
from application.helpers.gestor_restaurant import ManagerData

from application.models.Restaurant import Notifications, db

class NotificationsController:
    app = None
    managerData = ManagerData()
    def __init__(self) -> None:
        self.app = current_app

    def get_all(self, data):
        #require id_receiver and status
        ctn = []
        query = Notifications.query
        if "id_receiver" in data.keys():
            query = query.filter(Notifications.id_receiver == data["id_receiver"])
        if "level_receiver" in data.keys():
            query = query.filter(Notifications.level_receiver == data["level_receiver"])
        if "id_sender" in data.keys():
            query = query.filter(Notifications.id_sender == data["id_sender"])
        if "level_sender" in data.keys():
            query = query.filter(Notifications.level_sender_sender == data["level_sender"])
        if "state" in data.keys():
            query = query.filter(Notifications.status == data["state"])
        
        response = query.order_by(desc(Notifications.id)).all()
        if response:
            for data in response:
                ctn.append({
                    "id": data.id,
                    "created_at" : data.created_at,
                    "updated_at" : data.updated_at,
                    "id_sender" : data.id_sender,
                    "level_sender" : data.level_sender,
                    "id_receiver" : data.id_receiver,
                    "level_receiver" : data.level_receiver,
                    "title" : data.title,
                    "text" : data.text,
                    "link" : data.link,
                    "status" : data.status,
                })                

        return ctn
    
    def create(self, data=False):
        if data:
            prepared_data = Notifications(
                id_sender = data["id_sender"],
                level_sender = data["level_sender"],
                id_receiver = data["id_receiver"],
                level_receiver = data["level_receiver"],
                title = data["title"],
                text = data["text"],
                link = data["link"],
                status = 1,
            )
            
            db.session.add(prepared_data)
            db.session.commit()
            return "ok"
        return False
            
    # def update_status(self, data):
    #     new_status = data["status"]
    #     with self.app.app_context():
    #         if "id_admin" in data and "id_user" in data:
    #             id_user = data["id_user"]
    #             id_admin = self.managerData.email_to_id_admin()
    #             response = JobApplication.query.filter(JobApplication.id_user == id_user , JobApplication.id_admin == id_admin).first()
    #         elif "id_user" in data:
    #             id_user = self.managerData.email_to_id()
    #             response = JobApplication.query.filter(JobApplication.id_user == id_user).first()
    #         else:
    #             response = None

    #         if response is not None:
    #             response.job_status = new_status
    #         db.session.commit()
        
    #     return "ok"
    def delete(self, data):
        id_user = self.managerData.email_to_id()
        response = Notifications.query.filter(Notifications.id == data["id"], Notifications.id_receiver == id_user).first()
        if response:
            db.session.delete(response)
            db.session.commit()

        return "ok"