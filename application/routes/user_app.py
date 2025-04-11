import json
from flask import Blueprint, render_template, redirect, request, url_for, session, make_response, flash, send_file
from ..controllers.restaurant.foodDishes import Food
from ..controllers.restaurant.typeFoodABS import TypeFood_ABS
from ..controllers.restaurant.userController import UsersAdmin
from ..controllers.restaurant.usersAppController import UsersAppController
from ..controllers.restaurant.reservationsFoodsController import ReservationsFoodsController
from application.controllers.restaurant.dataSupportController import DataSupportController
from application.controllers.restaurant.dataOrderController import DataOrderController
from application.controllers.restaurant.orderDishes import Order
from application.controllers.restaurant.tableController import TableController
from application.controllers.restaurant.configurationDataController import ConfigurationDataController

from application.helpers.upload_files import UploadFiles
from application.helpers.gestor_restaurant import ManagerData
from application.helpers.appuser_manager import validated_user, userID
from application.helpers.mail_admin import sendEmail


managerData = ManagerData()
foodController = Food()
typeFoodController = TypeFood_ABS()
userController = UsersAdmin()
reservationsFoodsController = ReservationsFoodsController()
userAppController = UsersAppController()
dataSupportController = DataSupportController()
dataOrderController = DataOrderController()
orderController = Order()
tableController = TableController()
configurationDataController = ConfigurationDataController()
uploadFiles = UploadFiles()

PATH_UPLOAD_IMAGES_VOUCHERS = "application/views/static/images/userapp/vouchers_reservations/"
PATH_UPLOAD_IMAGES_PROFILE = "application/views/static/images/userapp/profile/"
PATH_UPLOAD_FILES_SUPPORT = "application/views/static/images/images_restaurant/files_support/"


user_app = Blueprint("user_app", __name__)

@user_app.route("/")
def login_user():
    if validated_user(): return redirect(url_for("user_app.home")) 

    return render_template("userapp/login.html")

@user_app.route("/credential_validation")
def credential_validation():
    number = request.args.get("number")
    password = request.args.get("password")
    
    response = userAppController.login_user(email=False, number=number.strip(), password=password.strip())
    
    if response:
        session["id"] = response.id
        return "ok"
    else:
        return "_"

    

@user_app.route("/create-account", methods=["GET", "POST"])
def create_account():
    if request.method == "POST":
        code = managerData.verification_code(cantity=4)
        cuerpo_email = f"""
            <div style="display: flex;justify-content: center;align-items:center;width:100%;height:100%;">
                <div style="width:100%; background-color:rgb(245, 245, 245);">
                    <div style="text-align: center;">
                        <span style='color:#fc9504;font-weight: 600;font-size: 1.3rem;'>{ code }</span><span style='font-size: 1.1rem;'> es su código de verificación.</span>
                    </div>
                    <div style="">
                        <p>Por favor, utiliza este código para verificar tu registro en Neeva. Este código es único y solo será válido por los próximos 10 minutos.</p>
                        <p>Si no has realizado este registro, por favor ignora este mensaje o contáctanos de inmediato a nuestro equipo de soporte.</p>
                        <p>Gracias por confiar en Neeva.</p>
                        <p>Atentamente, Neeva</p>
                    </div>
                </div>
            </div>
        """
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        tel_whats = request.form.get("tel_whats")
        password = request.form.get("password")
        response = userAppController.validate(email, tel_whats)
        if response == "ok":
            session["code"] = code
            session["first_name"] = first_name
            session["last_name"] = last_name
            session["email"] = email
            session["tel_whats"] = tel_whats
            session["password"] = password
            sendEmail(False, False, email, "CÓDIGO DE VERIFICACIÓN", cuerpo_email)
            return "ok"
            
        else:
            return response

    else:
        return render_template("userapp/create-account.html")
    
@user_app.route("/code_verification", methods=["GET"])
def code_verification():
    
    code_post = request.args.get("code_verification")
    if "code" in session:
        if session["code"] == code_post:
            new_id = userAppController.create({
                "first_name" : session["first_name"],
                "last_name" : session["last_name"],
                "email" : session["email"],
                "tel_whats" : session["tel_whats"],
                "password" : session["password"],
                "image" : "/static/images/userapp/profile/default-avatar-profile-icon.jpg",
                }
            )
            session["id"] = new_id
            return "ok"
        
    return "error"

@user_app.route("/redirect_home", methods=["GET"])
def redirect_home():
    max_a = 315360000
    cookie_cred_set = make_response(redirect(url_for("user_app.home")))
    # cookie_cred_set.set_cookie("user_email", session["email"], max_age = max_a)
    # cookie_cred_set.set_cookie("tel_whats", session["tel_whats"], max_age = max_a)
    cookie_cred_set.set_cookie("id", str(session["id"]), max_age = max_a)


    return cookie_cred_set


@user_app.route("/home")
def home():
    if not validated_user() : return redirect(url_for("user_app.login_user")) 
    
    response = userAppController.read({"id":userID()})
    if not response:
        return redirect(url_for("user_app.close_session")) 
    data_user_app = response[0]

    id_secondary = request.args.get("search")
    if not id_secondary:
        id_secondary = ""
        data = None
    else:
        data = userController.show_all({"id_secondary" : id_secondary.lower()})

    
    if data:
        res_u_a = userAppController.read({"id":request.cookies.get("id")})
        dataConfigAdmin = configurationDataController.read({"id_admin":data[0]["id"]})
        
        if res_u_a:
            if res_u_a[0]["favorite_admins"]:
                f = json.loads(res_u_a[0]["favorite_admins"])
                if int(data[0]["id"]) in f:
                    data[0]["favorite"] = 1
                else:
                    data[0]["favorite"] = 0
            else:
                data[0]["favorite"] = 0
        type_food_data = []
        if len(data) > 0:
            id_admin = data[0]["id"]
            type_food_data = typeFoodController.show_all({"id_admin":id_admin})
            for type_food in type_food_data:
                food_data = foodController.show_all_free({"id_type_food":type_food["id"]})
                type_food["foods_all"] = food_data
        else:
            print("sin datos")
        
        if data:
            data = data[0]

        data_render = {
            "dataConfigAdmin":dataConfigAdmin[0],
            "data_admin" : data,
            "type_food_data" : type_food_data,
            "search_value" : id_secondary,
        }
    else:
        profiles_admin = userController.read_admins_percentage({"id_secondary" : id_secondary})
        
        data_render = {
            "data_admins" : profiles_admin,
            "search_value" : id_secondary,
        }
    data_render["data_user_app"] = data_user_app
    return render_template("userapp/home.html", **data_render)

@user_app.route("/payments", methods=["POST", "GET"])
def payments_main():
    if not validated_user() : return redirect(url_for("user_app.login_user")) 
    data = request.form.get("products")
    
    if data:
        data_front = {"products":[], "amount_all":0}
        data_json = json.loads(data)
        tableData = []
        data_admin = {}
        dataConfigAdmin = {}
        if data_json:
            id_admin = data_json[0]["app"]
            dataConfigAdmin = configurationDataController.read({"id_admin":id_admin})[0]
            for f in data_json:
                food = foodController.show_all_free({"id_food": f["identifier"], "id_admin":id_admin})
                if food:
                    category_food = typeFoodController.show_all_free({"id_type_food":food[0]["type_food"], "id_admin":id_admin})
                    f["id"] = food[0]["id"]
                    f["food_name"] = food[0]["name"]
                    f["category_name"] = category_food[0]["name_type"]
                    f["food_image"] = food[0]["image"]
                    f["price_per_quantity"] = float(food[0]["price"]) * f["cantity"]
                    f["price_per_unit"] = food[0]["price"]
                    f["quantity"] = f["cantity"]
                    data_front["products"].append(f)
                    data_front["amount_all"] = data_front["amount_all"] + f["price_per_quantity"]

            data_admin = userController.show_all({"id_admin":id_admin})[0]
            tableData = tableController.read({"id_admin":id_admin})
            
        data_render = {
            "data_front":data_front,
            "data_admin":data_admin,
            "table_data":tableData,
            "dataConfigAdmin":dataConfigAdmin,
        }
        return render_template("userapp/pay_page.html", **data_render)
    else:
        return redirect(url_for("user_app.home"))
@user_app.route("/search_on_maps")
def search_on_map():
    if not validated_user() : return redirect(url_for("user_app.login_user")) 

    return render_template("userapp/location.html")

@user_app.route("/scan_qr")
def scan_qr():
    if not validated_user() : return redirect(url_for("user_app.login_user")) 

    return render_template("userapp/scan_qr.html")

@user_app.route("/reservations")
def reservations():
    if not validated_user() : return redirect(url_for("user_app.login_user")) 
    
    id_user = request.cookies.get("id")
    state_required = request.args.get("state")
    mode = request.args.get("mode")
    response_reservations = []
    # RESERVATIONs
    if state_required:
        if state_required == "all":
            response_reservations = reservationsFoodsController.get_all({"id_user" : id_user, "limit":6})
        else:
            response_reservations = reservationsFoodsController.get_all({"id_user" : id_user, "only_state":state_required, "limit":5})
    else:
        response_reservations = reservationsFoodsController.get_all({"id_user" : id_user, "limit":10})
    for response in response_reservations:
        total_price_products = 0
        new_data_products = []
        products_reservation = json.loads(response["foods_reservation"].replace("'", '"'))
        id_admin = False
        for product in products_reservation:
            id_food = product["identifier"]
            cantity = int(product["cantity"])
            id_admin = product["app"]  

            food_result = foodController.show_all_free({"id_food" : id_food, "id_admin" : id_admin})
            if food_result:
                food_result = foodController.show_all_free({"id_food" : id_food, "id_admin" : id_admin})[0]
                total_price_products = total_price_products + (float(food_result["price"]) * cantity)
                type_food = typeFoodController.show_all_free({"id_type_food" : food_result["type_food"]})
                if type_food:
                    type_food = typeFoodController.show_all_free({"id_type_food" : food_result["type_food"]})[0]
                    food_result["type_food"] = type_food["name_type"]
                    food_result["cantity"] = cantity
            new_data_products.append(food_result)
        if id_admin:
            dataConfigAdmin = configurationDataController.read({"id_admin":id_admin})
            response_admin = userController.show_all({"id_admin" : id_admin})[0]
            response["company_name"] = response_admin["company_name"]
            response["company_icon"] = response_admin["company_icon"]
            response["id_secondary"] = response_admin["id_secondary"]
            response["currency"] = dataConfigAdmin[0].currency

        response["foods_reservation"] = new_data_products
        response["total_price"] = total_price_products
            
    data_render = {
        "data_reservations" : response_reservations,
        "mode":mode,
    }
    return render_template("userapp/reservations.html", **data_render)

@user_app.route("/orders")
def orders():
    if not validated_user() : return redirect(url_for("user_app.login_user")) 
    
    id_user = request.cookies.get("id")
    state_required = request.args.get("state")
    mode = request.args.get("mode")
    number_table = None
    state_table = None
    order_table = []
    data_query = {"id_user_context":userID(),"limit":8, "user_level":5, "desc":True}
    if state_required:
        data_query["state_order"] = state_required
    # ORDER SECTION
    
    order_table = orderController.get_all_free(data_query)
    for order in order_table:
        admin_data = userController.show_all({"id_admin":order.id_user_admin})
        order.company_name = admin_data[0]["company_name"] if admin_data else "Error"
        order.company_icon = admin_data[0]["company_icon"] if admin_data else "Error"
        order.company_id_secondary = admin_data[0]["id_secondary"] if admin_data else "Error"
        dataConfigAdmin = configurationDataController.read({"id_admin":order.id_user_admin})
        order.currency = dataConfigAdmin[0].currency
        data_table = tableController.read({"id":order.id_table})
        if data_table:
            number_table = data_table[0].number_table
            state_table = data_table[0].state

            order.number_table = data_table[0].number_table
            id_user = order.id_user_context
            user_level = order.user_level
            order.total_cost = 0
            for d in order.data_orders:
                food_data = foodController.show_all_free({"id_food":d.id_food})
                if food_data:
                    d.food_name = food_data[0]["name"]
                    d.price = food_data[0]["price"]
                    d.image_food = food_data[0]["image"]
                    id_category = food_data[0]["type_food"]
                    cat_data = typeFoodController.show_all_free({"id_type_food":id_category})
                    d.category_name = cat_data[0]["name_type"]
                    order.total_cost = order.total_cost + (float(d.price) * int(d.quantity))
            
                d.observations = d.observation.split("///")
            
    data_render = {
        "order_table":order_table,
        "mode":mode,
    }
    
    return render_template("userapp/order.html", **data_render)
    
@user_app.route("/profile")
def profile():
    if not validated_user() : return redirect(url_for("user_app.login_user")) 
    id_user = request.cookies["id"]
    response = userAppController.read({"id":id_user})
    if response:
        new_favorite_admins=[]
        if response[0]["favorite_admins"]:
            favorite_admins = json.loads(response[0]["favorite_admins"])
            for admin in favorite_admins:
                res_user = userController.show_id(admin)
                new_favorite_admins.append(
                    {
                        "company_name":res_user["company_name"],
                        "company_icon":res_user["company_icon"],
                        "id_secondary":res_user["id_secondary"],
                        })
                
        response[0]["favorite_admins"] = new_favorite_admins
        data_render = response[0]
        return render_template("userapp/profile.html", **data_render)
    
    else:
        return redirect(url_for("user_app.close_session")) 


@user_app.route("/profile/edit_profile", methods = ["POST", "GET"])
def edit_profile():
    if not validated_user() : return redirect(url_for("user_app.login_user")) 
    id_user = request.cookies["id"]
    if request.method == "GET": 
        response = userAppController.read({"id":id_user})
        data_render = response[0]

        return render_template("userapp/edit_user_profile.html", **data_render)
    
    elif request.method == "POST":
        data = {}
        image = uploadFiles.uploadFile(request.files.get("image"), PATH_UPLOAD_IMAGES_PROFILE)
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        tel_whats = request.form.get("tel_whats")
        location = request.form.get("location")
        password = request.form.get("password")
        data["first_name"] = first_name
        data["last_name"] = last_name
        data["email"] = email
        data["tel_whats"] = tel_whats
        data["location"] = location
        if image:
            data["image"] = image
        if password:
            data["password"] = password
        
        r = userAppController.update(id_user, data)
        if r:
            return "ok"
        else:
            return "error"
        
@user_app.route("/favorities/add")
def favorities():
    if not validated_user() : return redirect(url_for("user_app.login_user")) 
    id_admin = request.args.get("to")    
    state = request.args.get("state")

    id_user_app = request.cookies.get("id")
    data_user_app = userAppController.read({"id":id_user_app})
    if data_user_app:
        favorities = data_user_app[0]["favorite_admins"]
        if favorities:
            favorities = json.loads(favorities)
            if int(state) == 1:
                if int(id_admin) not in favorities:
                    favorities.append(int(id_admin))
            elif int(state) == 0:
                if int(id_admin) in favorities:
                    favorities.remove(int(id_admin))
        else:
            if int(state) == 1:
                favorities = [int(id_admin)]

        res = userAppController.update(id_user_app, {"favorite_admins":str(favorities)})

    return "ok"

@user_app.route("/coordinates/get/for_map")
def for_map():
    if not validated_user() : return redirect(url_for("user_app.login_user")) 
    response_ = userController.show_all()
    data = []
    if response_:
        for user in response_:
            temp = {}
            temp["coordinates"] = user["company_location_coord"]
            temp["id_secondary"] = user["id_secondary"]
            data.append(temp)
    return data

@user_app.route("/support", methods=["GET","POST"])
def support():
    if not validated_user() : return redirect(url_for("user_app.login_user")) 
    if request.method == "GET":
        return render_template("userapp/support.html")
    elif request.method == "POST":
        email = userAppController.read({"id":userID()})[0]["email"]
        message = request.form.get("text_for_support")
        files = request.files.getlist("files_for_support")
        state_response_files = uploadFiles.uploadFile(files, PATH_UPLOAD_FILES_SUPPORT)
        response_controller = dataSupportController.create({
            "id_user" : userID(),
            "level_user" : 5,
            "email": email,
            "message": message,
            "files": json.dumps(state_response_files),
            "state" : 1,
        })
        if response_controller: 
            flash("Se ha enviado correctamente los datos.", "ok")
        else:
            flash("Ocurrió un error al enviar. Vuelva a enviar los datos por favor.", "error")

        return redirect(url_for("user_app.support"))
    else:
        return ""

@user_app.route("/service_worker_neeva.js")
def sw_mobile():
    return send_file('views/static/js/sw/service_worker_neeva.js')

@user_app.route("/order/save_order", methods=["POST"])
def saveOrder():
    if not validated_user() : return redirect(url_for("user_app.login_user")) 
    if request.json:
        data = request.get_json()
        d1 = {"state_order": 1, "id_user_admin":data["data"][0]["app"], "id_user_context":userID(), "order_code" : "", "user_level":5,"id_table":data["id_table"]}
        d1r = orderController.insert(d1)
        for f in data["data"]:
            d2 = {"id_admin" : data["data"][0]["app"], "id_food": f["identifier"], "quantity":f["cantity"], "observation":"", "order_dishes_id":d1r.id, "type_order":data["type_order"]}
            dataOrderController.insert(d2)
        order_code = str(d1r.id)+str(d1r.id_table)
        orderController.update(d1r.id, {"id_admin" : data["data"][0]["app"],"order_code":order_code})
        tableController.update(data["id_table"], {"state":2, "id_admin":data["data"][0]["app"]})
        return str(d1r.id)
    else:
        print("Error no json order")
        return {}


@user_app.route("/close_session")
def close_session():
    
    close_program = make_response(redirect(url_for("user_app.login_user")))
    close_program.delete_cookie("id")

    return close_program

