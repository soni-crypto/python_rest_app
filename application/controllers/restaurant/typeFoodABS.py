from sqlalchemy import desc
from flask import current_app
from application.models.Restaurant import TypeFoodABS, db
from application.helpers.gestor_restaurant import ManagerData
from application.controllers.restaurant.imageFoodController import ImageFoodController

managerData = ManagerData()
imageFoodController=ImageFoodController()
class TypeFood_ABS:
    app = current_app
    def show_all_free(self, data_for_filter={}):
        
        ctn=[]
        with self.app.app_context():
            data = TypeFoodABS.query
            if "id_admin" in data_for_filter.keys():
                data = data.filter(TypeFoodABS.id_user_admin == data_for_filter["id_admin"])
            if "id_type_food" in data_for_filter.keys():
                data = data.filter(TypeFoodABS.id == data_for_filter["id_type_food"])
            data = data.order_by(desc(TypeFoodABS.id)).all()
            for i in data:
                image_res=""
                resp=imageFoodController.show_all({"id":i.image})
                if len(resp)>0:
                    image_res=resp[0]["url_name"]
                else:
                    image_res = "/static/images/images_restaurant/onlyadmin/icon_food/default-folder.min.png"
                ctn.append({
                        "id" : i.id, 
                        "created_at" : i.created_at, 
                        "name_type" : i.name_type, 
                        "description" : i.description,
                        "image" : image_res, 
                        "state" : i.state,
                    })
            db.session.commit()
        return ctn
    
    def show_all(self, data_for_filter={}):
        if "id_admin" in data_for_filter.keys():
            id_user_context = data_for_filter["id_admin"]
        else:
            id_user_context = managerData.email_to_id_admin()
            
        ctn=[]
        with self.app.app_context():
            data = TypeFoodABS.query.filter(TypeFoodABS.id_user_admin == id_user_context).order_by(desc(TypeFoodABS.id)).all()
            for i in data:
                image_res=""
                resp=imageFoodController.show_all({"id":i.image})
                if len(resp)>0:
                    image_res=resp[0]["url_name"]
                else:
                    image_res = "/static/images/images_restaurant/onlyadmin/icon_food/default-folder.min.png"
                ctn.append({
                        "id" : i.id, 
                        "created_at" : i.created_at, 
                        "name_type" : i.name_type, 
                        "description" : i.description,
                        "image" : image_res, 
                        "state" : i.state,
                    })
            db.session.commit()
        return ctn
    def show_id(self, id):
        id_user_context = managerData.email_to_id_admin()
        ctn={}
        with self.app.app_context():
            # data = TypeFoodABS.query.get_or_404(id)
            data = TypeFoodABS.query.filter(TypeFoodABS.id == id, TypeFoodABS.id_user_admin == id_user_context).first()
            if data:
                ctn = {
                    "id" : data.id,
                    "created_at" : data.created_at,
                    "name_type" : data.name_type,
                    "description" : data.description,
                    "image" : data.image,
                    "state" : data.state,
                }
            db.session.commit()
        return ctn
    
    def delete(self, id):
        try:
            id_user_context = managerData.email_to_id_admin()
            with self.app.app_context():
                row = TypeFoodABS.query.filter(TypeFoodABS.id == id, TypeFoodABS.id_user_admin == id_user_context).first()
                if row:
                    db.session.delete(row)
                    db.session.commit()
            return "ok"
        except Exception as err:
            return "error"
    def update(self, id, data):
        id_user_context = managerData.email_to_id_admin()
        with self.app.app_context():
            row = TypeFoodABS.query.filter(TypeFoodABS.id == id, TypeFoodABS.id_user_admin == id_user_context).first()
            if row:
                # Actualiza todos los campos con los valores proporcionados en 'data'
                for key, value in data.items():
                    setattr(row, key, value)
                db.session.commit()
                return "ok"
            else:
                return "no hay datos"
    
    def insert(self, *args, **kwargs):
        id_user_context = managerData.email_to_id_admin()
        if (id_user_context == 0):
            return "not_linked"
        else:
            with self.app.app_context():
                data_full = TypeFoodABS(
                    name_type = kwargs["name_type"],
                    description = kwargs["description"],
                    image = kwargs["image"],
                    state = kwargs["state"],
                    id_user_admin = id_user_context,
                )
                db.session.add(data_full)
                db.session.commit()
            return "ok"