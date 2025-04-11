from flask import current_app
from application.models.Restaurant import AmountMainCollect, db
from application.helpers.gestor_restaurant import ManagerData
from application.controllers.restaurant.configurationDataController import ConfigurationDataController
import pytz

managerData = ManagerData()
configurationDataController = ConfigurationDataController()

class AmountCollect():
    app = current_app
    def show_all(self):
        id_user_context = managerData.email_to_id_admin()
        dataConfigAdmin = configurationDataController.read({"id_admin":id_user_context})[0]
        time_zone = pytz.timezone(dataConfigAdmin.time_zone) 
        ctn=[]
        with self.app.app_context():
            data = AmountMainCollect.query.filter(AmountMainCollect.id_user_admin == id_user_context).all()
            for i in data:
                i.created_at = i.created_at.astimezone(time_zone)
                ctn.append((i.id, i.created_at, i.amount_main, i.amount_diary))
            db.session.commit()
            
        return ctn
    
    def update(self, *args, **kwargs):
        id_user_context = managerData.email_to_id_admin()
        with self.app.app_context():
            data = AmountMainCollect.query.filter(AmountMainCollect.id_user_admin == id_user_context).all()
            if len(data) <=0:
                db.session.add(AmountMainCollect(
                    amount_main = 0, 
                    amount_diary = kwargs["amount_diary"], 
                    id_user_admin = id_user_context,
                    ))
            else:
                amount_old = data[0].amount_diary
                data[0].amount_diary = amount_old + kwargs["amount_diary"]
                
            db.session.commit()
        pass            
    def update_collect_main(self):
        id_user_context = managerData.email_to_id_admin()
        with self.app.app_context():
            data = AmountMainCollect.query.filter(AmountMainCollect.id_user_admin == id_user_context).all()
            if len(data) <=0:
                db.session.add(AmountMainCollect(
                    amount_main = 0, 
                    amount_diary = 0,
                    id_user_admin = id_user_context,
                    ))
            else:
                amount_main_old = data[0].amount_main
                amount_diary = data[0].amount_diary
                
                data[0].amount_main = amount_main_old + amount_diary
                data[0].amount_diary = 0
                
            db.session.commit()
            