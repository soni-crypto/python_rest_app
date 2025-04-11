from flask import current_app
from application.models.Restaurant import WaitressData, db
from sqlalchemy import desc

class WaitressMainC():
    app = current_app
    def show_all(self, data = {}):
        query = WaitressData.query
        if "id" in data.keys():
            query = query.filter(WaitressData.id == data["id"])
        if "partner_id" in data.keys():
            query = query.filter(WaitressData.partner_id == data["partner_id"])
        if "email" in data.keys():
            query = query.filter(WaitressData.user_email == data["email"])    
        if "box_id" in data.keys():
            query = query.filter(WaitressData.box_id == data["box_id"])    
    
        data_full = query.order_by(desc(WaitressData.id)).all()
            
        return data_full
    
    def waitress_insert(self, *args, **kwargs):
    
        data_full = WaitressData(
            user_role = kwargs["user_role"],
            user_first_name = kwargs["first_name"],
            user_last_name = kwargs["last_name"],
            user_phone_number = kwargs["phone_number"],
            user_email = kwargs["email"],
            user_password = kwargs["password"],
            user_image = kwargs["image"],
            partner_id = kwargs["partner_id"],
            box_id = kwargs["box_id"],
        )
        db.session.add(data_full)
        db.session.commit()
            
        return "ok"
    
    def waitress_update(self, data):
        
        row_selected = WaitressData.query.filter(WaitressData.id == data["id"], WaitressData.partner_id == data["id_admin"]).first()
        if row_selected:
            data.pop("id")
            data.pop("id_admin")
            for key, value in data.items():
                setattr(row_selected, key, value)                
            db.session.commit()
            return row_selected
        else:
            return False
        
    def waitress_delete(self, data):
        row_data = WaitressData.query.filter(WaitressData.id == data["id"], WaitressData.partner_id == data["id_admin"]).first()
        if row_data:
            db.session.delete(row_data)
            db.session.commit()
            return row_data
        else:
            return False