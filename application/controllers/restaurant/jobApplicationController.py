from flask import current_app

from application.helpers.gestor_restaurant import ManagerData

from application.models.Restaurant import JobApplication, db

class JobApplication_:
    app = None
    managerData = ManagerData()
    def __init__(self) -> None:
        self.app = current_app
    def get_all(self, status = 1):
        id_user = self.managerData.email_to_id()
        ctn = []
        response = JobApplication.query.filter(JobApplication.id_user == id_user, JobApplication.job_status == status).all()
        if response:
            for data in response:
                ctn.append({
                    "id": data.id,
                    "created_at" : data.created_at,
                    "updated_at" : data.updated_at,
                    "id_user" : data.id_user,
                    "id_admin" : data.id_admin,
                    "job_status" : data.job_status,
                })                

        return ctn
    
    def get_by_id(self):
        return ""
    def create(self, data):

        id_admin = self.managerData.email_to_id_admin()
        response = JobApplication.query.filter(JobApplication.id_user == data["id_user"], JobApplication.id_admin == id_admin).first()
        if response:
            if response.job_status == 0 or response.job_status == 2:
                response.job_status = 1
                db.session.commit()
            return "exists"
        else:
            prepared_data = JobApplication(
                id_user = data["id_user"],
                id_admin = id_admin,
                job_status = 1,
            )
            with self.app.app_context():
                db.session.add(prepared_data)
                db.session.commit()
            return "ok"
            
    def update_status(self, data):
        new_status = data["status"]
        with self.app.app_context():
            if "id_admin" in data and "id_user" in data:
                id_user = data["id_user"]
                id_admin = self.managerData.email_to_id_admin()
                response = JobApplication.query.filter(JobApplication.id_user == id_user , JobApplication.id_admin == id_admin).first()
            elif "id_admin" in data:
                id_admin = data["id_admin"]
                id_user = self.managerData.email_to_id()
                response = JobApplication.query.filter(JobApplication.id_user == id_user, JobApplication.id_admin == id_admin).first()
            else:
                response = None
            
            if response is not None:
                response.job_status = new_status
            db.session.commit()
        
        return "ok"
    def delete(self, data):
        id_admin = self.managerData.email_to_id_admin()
        response = JobApplication.query.filter(JobApplication.id_user == data["id_user"], JobApplication.id_admin == id_admin).first()
        if response:
            db.session.delete(response)
            db.session.commit()

        return "ok"