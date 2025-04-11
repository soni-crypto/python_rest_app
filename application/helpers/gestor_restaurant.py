import random
import cryptocode
from werkzeug.security import generate_password_hash, check_password_hash
from application.models.Restaurant import User, WaitressData
from flask import session, request, current_app, json
from application.controllers.restaurant.waitressController import WaitressMainC
from application.controllers.restaurant.userController import UsersAdmin

adminController = UsersAdmin()
waitressController = WaitressMainC()

class ManagerData():
    def verification_code(self, cantity = 6):
        code = ""
        for i in range(cantity):
            code = code + str(random.randint(0,9))
        return code
    
    def generate_random_letter(self, n_digitos = 10):
        letters=[1,2,3,4,5,6,7,8,9,0,'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        letras_aleatorias = [str(random.choice(letters)) for _ in range(n_digitos)]
        return ''.join(letras_aleatorias)
    
    def generate_hash(self, password):
        password_hashed = generate_password_hash(password)
        return password_hashed
    
    def check_hash(self, password_hash, password_db):
        s = check_password_hash(password_hash, password_db)
        if s:
            return True
        else:
            return False
    
    def encrypt_data(self, data):
        pass
    def decrypt_data(self, data):
        pass
    def email_to_id(self, email_new=None):
        
        id = None
        if email_new == None:
            email_temp = None
            if "user_email" in request.cookies:
                if request.cookies.get("user_email"):
                    email_temp = request.cookies.get("user_email")
            elif "user_email" in session:
                email_temp = session["user_email"]
                
            data_full = User.query.filter(User.user_email == email_temp).first()
            if data_full:
                id = data_full.id
            else:
                data_full = WaitressData.query.filter(WaitressData.user_email == email_temp).first()
                if data_full:
                    id = data_full.id
        else:
            data_full = User.query.filter(User.user_email == email_new).first()
            if data_full:
                id = data_full.id
            else:
                data_full = WaitressData.query.filter(WaitressData.user_email == email_new).first()
                if data_full:
                    id = data_full.id
                
        return id
    
    def email_to_id_admin(self, email_new=None):
        
        id = None
        if email_new == None:
            email_temp = None
            if "user_email" in request.cookies:
                if request.cookies.get("user_email"):
                    email_temp = request.cookies.get("user_email")
            elif "user_email" in session:
                email_temp = session["user_email"]
                
            data_full = User.query.filter(User.user_email == email_temp).first()
            if data_full:
                id = data_full.id
            else:
                data_full = waitressController.show_all({"email": email_temp})
                if data_full:
                    id = data_full[0].partner_id
        else:
            data_full = User.query.filter(User.user_email == email_new).first()
            if data_full:
                id = data_full.id
            else:
                data_full = waitressController.show_all({"email": email_new})
                if data_full:
                    id = data_full[0].partner_id
                
        return id
    def logged_user(self):
        if "user_email" in request.cookies or "user_email" in session:
            return True
        else:
            return False
        
    def validate_user_app(self, *args, **kwargs):
        user_email  = kwargs["email"]
        user_password = kwargs["password"]
        user_type = kwargs["type"]

        if int(user_type) == 4:
            data_user = WaitressData.query.filter(WaitressData.user_email == user_email, WaitressData.user_password == user_password).first()
        elif int(user_type) == 2:
            data_user = User.query.filter(User.user_email == user_email, User.user_password == user_password).first()
        else:
            return False
        
        if data_user:
            return data_user
        else:
            return False
            
    def validate_email(self, data={}):
        user_email = data["user_email"]
        user_type = data["user_type"]

        if int(user_type) == 4:
            data_user = WaitressData.query.filter(WaitressData.user_email == user_email).first()
        elif int(user_type) == 2:
            data_user = User.query.filter(User.user_email == user_email).first()
        else:
            return False
        
        if data_user:
            return data_user
        else:
            return False
        
    def image_name_saved_cookie_or_session(self):
        if "user_profile_image" in session:
            return session["user_profile_image"]
        if request.cookies.get("user_profile_image"):
            return request.cookies.get("user_profile_image")
        else:
            return "icon-main-emtorch.png"
    def level_saved_cookie_or_session(self):
        if "user_level_context" in session:
            return str(session["user_level_context"])
        if request.cookies.get("user_level_context"):
            return str(request.cookies.get("user_level_context"))
        else:
            return False
    
    def get_key_room_main(self):
        id = self.email_to_id_admin()
        response_data = User.query.filter(User.id == id).first()
        
        if response_data:
            return response_data.user_key_room_app
        else:
            return False
    
    def data_user_context (self):
        level = self.level_saved_cookie_or_session()
        id = self.email_to_id()
        data = {}
        if level:
            if str(level) == "2":
                data_ = User.query.filter(User.id == id).first()
                if data_ :
                    data = data_.__dict__
                    del(data["_sa_instance_state"])
                    del(data["user_password"])
                
            elif str(level) == "4":
                data_ = waitressController.show_all({"id":id})
                if data_ :
                    data = data_[0].__dict__
                    del(data["_sa_instance_state"])
                    del(data["user_password"])
        return data
    