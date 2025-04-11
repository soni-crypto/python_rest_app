from sqlalchemy import desc
from flask import current_app
from application.models.Restaurant import AvailableCountries, db

class availableCountries:
    app = current_app
    def get_everything(self, data={}):
        ctn=[]
        with self.app.app_context():
            query = AvailableCountries.query
            if "id" in data.keys():
                query = query.filter(AvailableCountries.id == data["id"]) 
            data = query.order_by(desc(AvailableCountries.id)).all()
            for i in data:
                ctn.append({
                    "id" : i.id, 
                    "created_at" : i.created_at,
                    "country_name" :  i.country_name,
                    "country_image" : i.country_image,
                    "country_code" : i.country_code,
                    "country_state" : i.country_state,
                })
            db.session.commit()
        return ctn
    
    def insert(self, data=False):
        if data:
        
            prepared = AvailableCountries(
                country_name = data["country_name"],
                country_image = data["country_image"],
                country_code = data["country_code"],
                country_state = data["country_state"],
            )
            
            db.session.add(prepared)
            db.session.commit()
        
            return prepared
        else:
            return {"error":"data not found"}
    
    def delete(self, id):
    
        row = AvailableCountries.query.filter(AvailableCountries.id == id).first()
        
        if row:
            db.session.delete(row)
            db.session.commit()
        
        return row
    
    def update(self, id, data):
        
        row_full = AvailableCountries.query.filter(AvailableCountries.id == int(id)).first()
        
        if row_full:
            for key, value in data.items():
                setattr(row_full, key, value)
            db.session.commit()
        
        return row_full
    