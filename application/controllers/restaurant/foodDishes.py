from sqlalchemy import desc
from flask import current_app
from application.models.Restaurant import FoodDishes, db
from application.helpers.gestor_restaurant import ManagerData
from application.controllers.restaurant.imageFoodController import ImageFoodController
import time
managerData = ManagerData()
imageFoodController=ImageFoodController()

class Food:
    app = current_app
    def show_all_free(self, data_for_filter={}, get_instance=False):
        ctn=[]
        with self.app.app_context():
            query = FoodDishes.query
            if "id" in data_for_filter.keys():
                query = query.filter(FoodDishes.id == data_for_filter["id"])
            if "id_type_food" in data_for_filter.keys():
                query = query.filter(FoodDishes.type_food == data_for_filter["id_type_food"])
            if "id_food" in data_for_filter.keys():
                query = query.filter(FoodDishes.id == data_for_filter["id_food"])
            if "id_admin" in data_for_filter.keys():
                query = query.filter(FoodDishes.id_user_admin == data_for_filter["id_admin"])

            data = query.order_by(desc(FoodDishes.id)).all()

            for i in data:
                image_res=""
                resp=imageFoodController.show_all({"id":i.image})
                
                if resp:
                    image_res=resp[0]["url_name"]
                else:
                    image_res = "/static/images/images_restaurant/onlyadmin/icon_food/default-food.min.png"
                ctn.append(
                    {
                        "id" : i.id,
                        "created_at" : i.created_at, 
                        "name" : i.name,
                        "description" :  i.description,
                        "type_food" : i.type_food ,
                        "price" : i.price,
                        "preparation_time" : i.preparation_time,
                        "product_code" : i.product_code,
                        "image" : image_res,
                        "state" : i.state,
                        "id_user_admin" : i.id_user_admin,
                    }
                    )
            db.session.commit()
        return ctn
    
    def show_all(self, data_filter={}):
        ctn=[]
        if "id_admin" in data_filter:
            id_user_context = data_filter["id_admin"]
        else:
            id_user_context = managerData.email_to_id_admin()
        with self.app.app_context():
            
            data = FoodDishes.query.filter(FoodDishes.id_user_admin == id_user_context).order_by(desc(FoodDishes.id)).all()
            for i in data:
                ctn.append(
                    {
                        "id" : i.id, 
                        "name" : i.name,
                        "description" :  i.description,
                        "type_food" : i.type_food ,
                        "price" : i.price,
                        "preparation_time" : i.preparation_time,
                        "product_code" : i.product_code,
                        "image" : i.image,
                        "state" : i.state,
                        "id_user_admin" : i.id_user_admin,
                    }
                    )
            db.session.commit()
        return ctn
    
    def show_id(self, id):
        id_user_context = managerData.email_to_id_admin()
        ctn={}
        with self.app.app_context():
            
            # data = FoodDishes.query.get_or_404(id)
            data = FoodDishes.query.filter(FoodDishes.id == id, FoodDishes.id_user_admin == id_user_context ).first()
            if data:
                ctn = {
                        "id": data.id,
                        "name": data.name,
                        "description": data.description,
                        "type_food": data.type_food,
                        "price": data.price,
                        "preparation_time" : data.preparation_time,
                        "product_code" : data.product_code,
                        "image" : data.image,
                        "state" : data.state,
                        "id_user_admin" : data.id_user_admin,
                    }
            db.session.commit()
        return ctn
    
    def show_type_food(self, id):
        id_user_context = managerData.email_to_id_admin()
        ctn=[]    
        data = FoodDishes.query.filter(FoodDishes.type_food == id, FoodDishes.id_user_admin == id_user_context).all()
        for i in data:
            image_res=""
            resp=imageFoodController.show_all({"id":i.image})
            if len(resp)>0:
                image_res=resp[0]["url_name"]
            ctn.append({
                "id" : i.id, 
                "name" : i.name, 
                "description" : i.description,
                "type_food" : i.type_food , 
                "price" : i.price, 
                "preparation_time" : i.preparation_time,
                "product_code" : i.product_code,
                "image" : image_res, 
                "state" : i.state
                })
        
        return ctn
        
    def insert(self, *args, **kwargs):
        id_user_context = managerData.email_to_id_admin()
        with self.app.app_context():
            mod = FoodDishes(
                name = kwargs["name"],
                description = kwargs["description"],
                type_food = kwargs["type_food"],
                price = kwargs["price"],
                product_code = kwargs["product_code"],
                image = kwargs["image"],
                state = kwargs["state"],
                preparation_time = kwargs["preparation_time"],
                id_user_admin = id_user_context,
            )
            
            db.session.add(mod)
            db.session.commit()
        
        return {"state":200}
    
    def delete(self, id):
        id_user_context = managerData.email_to_id_admin()
        with self.app.app_context():
            fila = FoodDishes.query.filter(FoodDishes.id == id, FoodDishes.id_user_admin == id_user_context).first()
            
            if fila != None:
                db.session.delete(fila)
                db.session.commit()
                return {"state":200}
        
        return {"state":"error"}
    
    def update(self, id, data):
        id_user_context = managerData.email_to_id_admin()
        
        with self.app.app_context():
            
            row_full = FoodDishes.query.filter(FoodDishes.id == int(id), FoodDishes.id_user_admin == id_user_context).first()
            
            if row_full:
                for key, value in data.items():
                    setattr(row_full, key, value)
                db.session.commit()
                return("ok")
                
            else:
                return "error"
        
        