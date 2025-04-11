from flask import current_app
from application.helpers.gestor_restaurant import ManagerData
from application.models.Restaurant import Jobs, db
class JobsController :
    app = current_app
    jobs = Jobs()
    managerData = ManagerData()
    def get_all(self):
        id_admin = self.managerData.email_to_id_admin()
        response = Jobs.query.filter(Jobs.id_admin == id_admin).all()
        data_dict = []        
        for job in response:
            dict_prepared = job.__dict__
            del(dict_prepared["_sa_instance_state"])
            data_dict.append(dict_prepared)
            
        return data_dict
    def get_filter(self, data=False):
        
        if data:
            keyword = data["keyword"]  
            location = data["location"]
            job_type = data["job_type"]
            job_salary_time = data["job_salary_time"]

            query = Jobs.query
            if keyword:
                query = query.filter(Jobs.job_title.like(f"%{keyword}%"))
            if location:
                query = query.filter(Jobs.job_location.like(f"%{location}%"))
            if job_type:
                query = query.filter(Jobs.job_type == job_type)
            if job_salary_time:
                query = query.filter(Jobs.job_salary_time == job_salary_time)

            response = query.all()
        else:
            response = Jobs.query.all()

        data_dict = []        
        for job in response:
            dict_prepared = job.__dict__
            del(dict_prepared["_sa_instance_state"])
            data_dict.append(dict_prepared)

        return data_dict
    
    def create_job(self, data = False):
        # with self.app.app_context():
        if data:
            prepared_data = Jobs(
                id_admin = data["id_admin"],
                job_title = data["job_title"],
                job_details = data["job_details"],
                job_location = data["job_location"],
                job_maximum_salary = data["job_maximum_salary"],
                job_minimum_salary = data["job_minimum_salary"],
                job_salary_time = data["job_salary_time"],
                job_type = data["job_type"],
            )
            db.session.add(prepared_data)
            db.session.commit()

        return "ok"