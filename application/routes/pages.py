from flask import Blueprint, render_template, send_file, session, redirect, make_response, request, url_for, flash
from application.controllers.restaurant.userController import UsersAdmin
from application.controllers.restaurant.waitressController import WaitressMainC
from application.helpers.gestor_restaurant import ManagerData
import datetime

pages = Blueprint("pages", __name__)
usersModel = UsersAdmin()
waitressModel = WaitressMainC()
managerData = ManagerData()

@pages.route("/")
def start():
    return render_template("home/pages/index.html")

@pages.route("/download/app")
def downloadApp():
    return render_template("home/pages/download_app.html")

@pages.route("/emtorch-sw-0.0.1.js")
def sw_mobile():
    return send_file('views/static/js/sw/emtorch-sw-0.0.1.js')

@pages.route("/offline-template-app-neeva")
def offline_adm():
    return render_template("pages/without_internet_connection.html")

@pages.route("/google06f1e2c0c11889f4.html")
def search_google():
    return render_template("pages/google06f1e2c0c11889f4.html")

@pages.route("/login", methods = ["GET", "POST"])
def loginApp():
    if request.method == "GET":
        if request.cookies.get("user_email") or "user_email" in session:
            return redirect(url_for("restaurant.reportAll"))
        msg = request.args.get("s")
        if msg:
            return render_template("pages/login.html", message = "user_not_found")
        
        else:
            return render_template("pages/login.html")
    
    elif request.method == "POST":
        email_ = request.form.get("email")
        password_ = request.form.get("password")
        save_cred = request.form.get("save-cred")
        type_ = request.form.get("mode")
        
        data_user_w = managerData.validate_user_app(email=email_, password=password_, type=type_)
        
        if data_user_w:
            if str(type_) == "4":
                if data_user_w.user_role == 1 or data_user_w.user_role == 2:
                    pass
                else:
                    return redirect(url_for("pages.loginApp", s = "403"))

            image_profile_main_user = data_user_w.user_image
            user_level_context = data_user_w.user_type
            if save_cred == "on":
                
                max_a = 14 * 24 * 60 * 60
                cookie_cred_set = make_response(redirect(url_for("restaurant.reportAll")))
                cookie_cred_set.set_cookie("user_email", email_, max_age = max_a)
                cookie_cred_set.set_cookie("user_profile_image", image_profile_main_user, max_age = max_a)
                cookie_cred_set.set_cookie("user_level_context", str(user_level_context) , max_age = max_a)
                
                return cookie_cred_set
            
            session["user_email"] = email_
            session["user_profile_image"] = image_profile_main_user
            session["user_level_context"] = user_level_context
            
            return redirect(url_for("restaurant.reportAll"))
        else:
            return redirect(url_for("pages.loginApp", s = "403"))
        
@pages.route("/register", methods = ["GET", "POST"])
def createUserAdmin():
    if request.method == "GET":
        
        if request.cookies.get("user_email") or "user_email" in session:
            return redirect(url_for("restaurant.reportAll"))
    
        else:
            return render_template("pages/create_account_admin.html")
    
    elif request.method == "POST":
        type_client = 2 #request.form.get("type_client")
        names_ = request.form.get("names")
        surnames_ = request.form.get("surnames")
        email_ = request.form.get("email")
        telephone_ = request.form.get("telephone")
        password_ = request.form.get("password")
        images_profile = "default-avatar-profile-icon.jpg"
        
        respuesta_email = managerData.validate_email({"user_email":email_, "user_type":type_client})
        
        if (not respuesta_email):
            fecha_actual = datetime.datetime.utcnow()
            dia_actual = fecha_actual.day
            if fecha_actual.month == 12:
                nuevo_mes = 1
                nuevo_ano = fecha_actual.year + 1
            else:
                nuevo_mes = fecha_actual.month + 1
                nuevo_ano = fecha_actual.year
            subscription_end_date_ = datetime.datetime(nuevo_ano, nuevo_mes, dia_actual)
            if (int(type_client) == 2):
                res = usersModel.insert_user(
                        subscription_end_date = subscription_end_date_,
                        user_name = names_,
                        user_surnames = surnames_,
                        user_email = email_,
                        user_number = telephone_,
                        user_password = password_,
                        user_image = images_profile,
                        user_key_room_app = ""
                    )
                
                usersModel.user_update(res.id, {"user_key_room_app":str(res.id)+managerData.generate_random_letter(16)})
                
            elif (int(type_client) == 4):
                status = waitressModel.waitress_insert(
                    first_name = names_,
                    last_name = surnames_,
                    phone_number = telephone_,
                    email = email_,
                    password = password_,
                    image = images_profile,
                    partner_id = 0,
                )
            return redirect(url_for("pages.loginApp"))
        else:
            flash("El correo ya está en uso")
            return redirect(url_for("pages.createUserAdmin"))
        
