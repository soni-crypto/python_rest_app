from sqlalchemy import desc
from flask import current_app
from application.models.Restaurant import ImageFood, db
from application.helpers.gestor_restaurant import ManagerData

managerData = ManagerData()

class ImageFoodController:
    app = current_app
    def show_all(self, data_for_filter={}):
        
        ctn=[]
        with self.app.app_context():
            data = ImageFood.query
            if "id_admin" in data_for_filter.keys():
                data = data.filter(ImageFood.id_admin == data_for_filter["id_admin"])
            if "id_type_food" in data_for_filter.keys():
                data = data.filter(ImageFood.id == data_for_filter["id_type_food"])
            if "word_to_search" in data_for_filter.keys():
                data = data.filter(ImageFood.name.like(f'{data_for_filter["word_to_search"]}%'))
            if "id" in data_for_filter.keys():
                data = data.filter(ImageFood.id == data_for_filter["id"])
            if "limit" in data_for_filter.keys():
                data = data.order_by(desc(ImageFood.id)).limit(data_for_filter["limit"]).all()
            else:
                data = data.order_by(desc(ImageFood.id)).limit(6).all()

            for i in data:
                dict_temp = i.__dict__
                del(dict_temp["_sa_instance_state"])
                del(dict_temp["updated_at"])
                del(dict_temp["created_at"])
                ctn.append(dict_temp)
        return ctn

    def delete(self, id):
        try:
            with self.app.app_context():
                row = ImageFood.query.filter(ImageFood.id == id).first()
                if row:
                    db.session.delete(row)
                    db.session.commit()
            return "ok"
        except Exception as err:
            return "error"
        
    def update(self, id, data):
        with self.app.app_context():
            row = ImageFood.query.filter(ImageFood.id == id).first()
            if row:
                # Actualiza todos los campos con los valores proporcionados en 'data'
                for key, value in data.items():
                    setattr(row, key, value)
                db.session.commit()
                return "ok"
            else:
                return "no hay datos"
    
    def insert(self, data_json):
        with self.app.app_context():
            data_prepared = ImageFood(
                id_admin = data_json["id_admin"],
                name = data_json["name"],
                url_name = data_json["url_name"],
                state = 1
            )
            db.session.add(data_prepared)
            db.session.commit()
        return "ok"