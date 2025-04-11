
from flask import Blueprint, render_template, send_file, session, redirect, make_response, request, url_for, flash
from application.helpers.gestor_restaurant import ManagerData
from application.controllers.restaurant.userController import UsersAdmin
from application.controllers.restaurant.waitressController import WaitressMainC
from application.controllers.restaurant.typeFoodABS import TypeFood_ABS
from application.controllers.restaurant.foodDishes import Food
from application.controllers.restaurant.availabilityCalendarController import AvailabilityCalendarController
from application.controllers.restaurant.configurationDataController import ConfigurationDataController
from application.controllers.restaurant.tableCategoryController import TableCategoryController
from application.controllers.restaurant.tableController import TableController
from application.controllers.restaurant.dataOrderController import DataOrderController
from application.controllers.restaurant.orderDishes import Order
from application.controllers.restaurant.freeUserController import FreeUserController

import datetime

page_client = Blueprint("page_client", __name__)
managerData = ManagerData()
adminController = UsersAdmin()
userController = WaitressMainC()
categoryFoodController = TypeFood_ABS()
foodController = Food()
availabilityCalendarController = AvailabilityCalendarController()
configurationDataController = ConfigurationDataController()
tableCategoryController = TableCategoryController()
tableController = TableController()
dataOrderController = DataOrderController()
orderModel = Order()
freeUserController = FreeUserController()

@page_client.context_processor
def data_in_session ():
    data_admin_session = {}
    if "id_secondary" in session and "id_admin" in session:
        data_admin_session["id_secondary"] = session["id_secondary"]
        data_admin_session["id_admin"] = session["id_admin"]
        
        conf = configurationDataController.read({"id_admin":session["id_admin"]})
        data_admin_session["maximum_distance_range"] = conf[0].maximum_distance_range
        data_admin_session["price_per_delivery"] = conf[0].price_per_delivery
        data_admin_session["currency"] = conf[0].currency

    return dict(data_admin_session = data_admin_session)

@page_client.route("/<id_secondary>")
def home(id_secondary):
    data_send = {}
    if id_secondary:
        data_admin = adminController.show_all({"id_secondary":id_secondary})
        if data_admin:
            data_admin = data_admin[0]
            session["id_secondary"] = id_secondary
            session["id_admin"] = data_admin["id"]
            del(data_admin["subscription_start_date"])
            del(data_admin["subscription_end_date"])
            del(data_admin["created_at"])
            del(data_admin["updated_at"])
            data_food_category = categoryFoodController.show_all_free({"id_admin": data_admin["id"]})
            data_food = foodController.show_all_free({"id_admin":data_admin["id"]})
            if data_food_category and data_food:
                for c in data_food_category:
                    c["foods"] = []
                    for f in data_food:
                        if c["id"] == f["type_food"]:
                            del(f["created_at"])
                            del(f["id_user_admin"])
                            del(f["product_code"])
                            c["foods"].append(f)
                    del(c["created_at"])
                    del(c["image"])
                    
            data_send["categories_food"] = data_food_category
            del(data_admin["id"])
            del(data_admin["user_key_room_app"])
            del(data_admin["user_type"])
            data_send["data_admin"] = data_admin
            
            return render_template("page_client/index.html", **data_send)
    return {"error" : 404}


@page_client.route("/<i_s>/cart")
def cart(i_s):
    if "id_secondary" in session:
        id_secondary = session["id_secondary"]
        if id_secondary == i_s:
            return render_template("page_client/cart.html")
    
    return redirect(url_for("page_client.home", id_secondary = "404"))

@page_client.route("/<i_s>/table")
def table(i_s):
    if "id_secondary" in session:
        id_secondary = session["id_secondary"]
        if id_secondary == i_s:
            data_admin = adminController.show_all({"id_secondary":id_secondary})[0]
            table = tableController.read({"id_admin":data_admin["id"]})
            table_category = tableCategoryController.read({"id_admin":data_admin["id"]})
            return render_template("page_client/table.html", table = table, table_category = table_category)
    
    return redirect(url_for("page_client.home", id_secondary = "404"))

@page_client.route("/<i_s>/calendar")
def calendar(i_s):
    if "id_secondary" in session and "id_admin" in session:
        id_secondary = session["id_secondary"]
        if id_secondary == i_s:
            return render_template("page_client/calendar.html")
    return redirect(url_for("page_client.home", id_secondary = "404"))

@page_client.route("/get/calendar/data")
def calendar_data():
    data_json = []
    if "id_secondary" in session and "id_admin" in session:
        id_admin = session["id_admin"]
        date_time_now = datetime.datetime.now()
        data = availabilityCalendarController.read({"id_admin":id_admin , "date_start":date_time_now})
        data_json = []
        for d in data:
            data_json.append(d.__dict__)
        
        list_del = ["_sa_instance_state", "created_at", "updated_at", "id_admin"]
        for d in data_json:
            if "T" in d["end"]:
                d["allDay"] = False
            if d["state"] == 0:
                d["display"] = "background"
            for k in list(d.keys()): 
                if not d[k] or k in list_del:
                    del(d[k])
    
    return data_json

@page_client.route("/<i_s>/delivery")
def delivery(i_s):
    if "id_secondary" in session and "id_admin" in session:
        id_secondary = session["id_secondary"]
        if id_secondary == i_s:
            data_admin = {}
            dataConfigAdmin = {}
            d_admin = adminController.show_all({"id_admin":session["id_admin"]})
            
            if d_admin:
                d_admin = d_admin[0]
                data_admin["company_location_coord"] = d_admin["company_location_coord"]
                conf = configurationDataController.read({"id_admin":session["id_admin"]})
                dataConfigAdmin["maximum_distance_range"] = conf[0].maximum_distance_range
                dataConfigAdmin["price_per_delivery"] = conf[0].price_per_delivery
                dataConfigAdmin["currency"] = conf[0].currency

            return render_template("page_client/location.html", data_admin = data_admin, dataConfigAdmin = dataConfigAdmin)
    return redirect(url_for("page_client.home",id_secondary = "404"))

@page_client.route("/<i_s>/checkout")
def checkout_app(i_s):
    if "id_secondary" in session and "id_admin" in session:
        id_secondary = session["id_secondary"]
        if id_secondary == i_s:

            return render_template("page_client/checkout_app.html")


@page_client.route("/<i_s>/save_data", methods=["POST"])
def save_data(i_s):
    if "id_secondary" in session and "id_admin" in session:
        id_secondary = session["id_secondary"]
        if id_secondary == i_s:
            id_admin = session["id_admin"]
            jdapp = request.get_json()
            id_table = jdapp["data"]["table"]
            type_request = jdapp["data"]["category"]
            data_json_order = jdapp["products"]
            response_free_user = freeUserController.insert({
                "id_admin":id_admin,
                "user_level" : 6,
                "name" : jdapp["data"]["user_name"] + ", " + jdapp["data"]["user_surnames"],
                "phone_number" : jdapp["data"]["user_telephone"],
                "email" : jdapp["data"]["user_email"],
                "address" : jdapp["data"]["delivery_address"],
            })
            
            d1 = {"state_order": 1, "id_user_admin": id_admin, "id_user_context" : response_free_user.id, "order_code":"", "user_level": 6, "id_table":id_table}
            d1r = orderModel.insert(d1)

            for f in data_json_order:
                category = foodController.show_all_free({"id" : f["product"]})[0]["type_food"]
                d2 = {"id_admin":id_admin, "id_food": f["product"], "quantity":f["quantity"], "observation":jdapp["data"]["message"], "order_dishes_id":d1r.id, "type_order":category}
                dataOrderController.insert(d2)
            order_code = str(d1r.id)+str(d1r.id_table)
            orderModel.update(d1r.id, {"id_admin" : id_admin,"order_code":order_code})

            # tableController.update(id_table, {"state":2, "id_admin": ""})

            return i_s

@page_client.route("/<i_s>/thanks")
def thanks(i_s):
    if "id_secondary" in session and "id_admin" in session:
        id_secondary = session["id_secondary"]
        if id_secondary == i_s:

            return render_template("page_client/checkout_app.html")



















@page_client.route("/api/get/data_for_page")
def data_for_page(id_secondary):
    data_send = {}
    if id_secondary:
        data_admin = adminController.show_all({"id_secondary":id_secondary})
        if data_admin:
            data_admin = data_admin[0]
            del(data_admin["subscription_start_date"])
            del(data_admin["subscription_end_date"])
            del(data_admin["created_at"])
            del(data_admin["updated_at"])
            data_food_category = categoryFoodController.show_all_free({"id_admin": data_admin["id"]})
            data_food = foodController.show_all_free({"id_admin":data_admin["id"]})
            if data_food_category and data_food:
                for c in data_food_category:
                    c["foods"] = []
                    for f in data_food:
                        if c["id"] == f["type_food"]:
                            del(f["created_at"])
                            del(f["id_user_admin"])
                            del(f["product_code"])
                            c["foods"].append(f)
                    del(c["created_at"])
                    del(c["image"])
                    
            data_send["categories_food"] = data_food_category
            del(data_admin["id"])
            del(data_admin["user_key_room_app"])
            del(data_admin["user_type"])
            data_send["data_admin"] = data_admin

    return data_send