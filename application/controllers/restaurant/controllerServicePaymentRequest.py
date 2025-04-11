from application.models.Restaurant import ServicePaymentRequest, db
from flask import current_app
class ControllerServicePaymentRequest:
    app = current_app
    def read(self, data_filter:dict = {} ) -> list:
        list_data = []
        query = ServicePaymentRequest.query

        data_all = query.all()
        for data in data_all:
            data_dict = data.__dict__
            del(data_dict["_sa_instance_state"])
            list_data.append(data_dict)
            
        return list_data
    
    def create(self, data:dict) -> str:
        with self.app.app_context():
            data_prepared = ServicePaymentRequest()
            for key, value in data.items():
                setattr(data_prepared, key, value)
            db.session.add(data_prepared)
            db.session.commit()
        return ""
    
    def update(self, data_filter:dict, data:dict) -> str:
        return ""

    def delete(self, data_filter:dict) -> str:
        return ""