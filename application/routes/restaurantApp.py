import json
from ..controllers.restaurant.orderDishes import Order
from ..controllers.restaurant.foodDishes import Food
from ..controllers.restaurant.typeFoodABS import TypeFood_ABS
from ..controllers.restaurant.amountCollect import AmountCollect
from ..controllers.restaurant.userController import UsersAdmin
from ..controllers.restaurant.historyController import StockHistoryC
from ..controllers.restaurant.waitressController import WaitressMainC
from ..controllers.restaurant.jobApplicationController import JobApplication_
from ..controllers.restaurant.notificationsController import NotificationsController
from ..controllers.restaurant.availableCountries import availableCountries
from ..controllers.restaurant.commentsFood import CommentsFoodController
from ..controllers.restaurant.reservationsFoodsController import ReservationsFoodsController
from ..controllers.restaurant.usersAppController import UsersAppController
from ..controllers.restaurant.dataSupportController import DataSupportController
from ..controllers.restaurant.restaurantBoxController import RestaurantBoxController
from application.controllers.restaurant.tableController import TableController
from application.controllers.restaurant.dataOrderController import DataOrderController
from application.controllers.restaurant.configurationDataController import ConfigurationDataController
from application.controllers.restaurant.tableCategoryController import TableCategoryController
from application.controllers.restaurant.inventoryController import InventoryController
from application.controllers.restaurant.categoryInventoryController import InventoryCategoryController
from application.controllers.restaurant.customerInventoryController import CustomerInventoryController
from application.controllers.restaurant.supplierInventoryController import SupplierInventoryController
from application.controllers.restaurant.salesInventoryController import SalesInventoryController
from application.controllers.restaurant.paymentOrderController import PaymentOrderController
from application.controllers.restaurant.freeUserController import FreeUserController
from application.controllers.restaurant.mainBoxRestaurantController import MainBoxRestaurantController
from application.controllers.restaurant.incomeAndExpenditureBoxController import IncomeAndExpenditureBoxController
from application.controllers.restaurant.availabilityCalendarController import AvailabilityCalendarController
from application.controllers.restaurant.imageFoodController import ImageFoodController

from application.helpers.gestor_restaurant import ManagerData
from application.helpers.upload_files import UploadFiles
from application.helpers.qr_code_generator import qr_code_generator
from application.helpers.config_tz import get_current_country_date_time
from application.helpers.mail_admin import sendEmail
import pytz
import datetime

from flask import Blueprint, render_template, redirect, url_for, request, session, make_response, flash, get_flashed_messages, jsonify, current_app
import os

restaurant = Blueprint("restaurant",__name__)
orderModel = Order()
foodModel = Food()
typeFoodModel = TypeFood_ABS()
amountModel = AmountCollect()
usersModel = UsersAdmin()
recordModel = StockHistoryC()
waitressModel = WaitressMainC()
jobApplication_c = JobApplication_()
notificationsController = NotificationsController()
countriesController = availableCountries()
managerData = ManagerData()
uploadFiles = UploadFiles()
commentsFoodController = CommentsFoodController()
reservationsFoodsController = ReservationsFoodsController()
userAppController = UsersAppController()
dataSupportController = DataSupportController()
restaurantBoxController = RestaurantBoxController()
tableController = TableController()
dataOrderController = DataOrderController()
configurationDataController = ConfigurationDataController()
tableCategoryController = TableCategoryController()
inventoryController = InventoryController()
inventoryCategoryController = InventoryCategoryController()
customerInventoryController = CustomerInventoryController()
supplierInventoryController = SupplierInventoryController()
salesInventoryController = SalesInventoryController()
paymentOrderController = PaymentOrderController()
freeUserController = FreeUserController()
mainBoxRestaurantController = MainBoxRestaurantController()
incomeAndExpenditureBoxController = IncomeAndExpenditureBoxController()
availabilityCalendarController = AvailabilityCalendarController()

imageFoodController = ImageFoodController()

PATH_UPLOAD_IMAGES_FOODS = "application/views/static/images/images_restaurant/images_upload/"
PATH_UPLOAD_IMAGES_USERS = "application/views/static/images/images_restaurant/images_profiles/"
PATH_UPLOAD_ICONS_PARTNER = "application/views/static/images/images_restaurant/icons_partner/"
PATH_UPLOAD_IMAGE_PAY_METHODS = "application/views/static/images/images_restaurant/images_pay-app/"
PATH_UPLOAD_FILES_SUPPORT = "application/views/static/images/images_restaurant/files_support/"
PATH_UPLOAD_QR_CODE = "application/views/static/images/images_restaurant/qr_code_admin/"
PATH_UPLOAD_ICONS_FOOD = "application/views/static/images/images_restaurant/onlyadmin/icon_food/"

@restaurant.context_processor
def default_process():
    app_settings = {}
    admin_settings = {}
    super_admin_settings = {}
    id_admin=managerData.email_to_id_admin()
    user_data_context = managerData.data_user_context()
    if id_admin:
        admin_settings = configurationDataController.read({"id_admin":id_admin})[0]
        current_app.config["TIME_ZONE"] = admin_settings.time_zone

    return dict(app_settings=app_settings, admin_settings=admin_settings, user_data_context = user_data_context)

# EDIT USERS ADMIN WAITRESS
@restaurant.route("/update_id_secondary", methods = ["GET"])
def update_id_secondary():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    id_secondary = request.args.get("value")
    
    userAdmin = usersModel.show_all({
        "id_secondary" : id_secondary.lower(),
    })
    if len(userAdmin) > 0:
        return("not_available")
    else:
        return("ok")

@restaurant.route("/edit_user_admin", methods = ["GET", "POST"])
def editUserAdmin_1():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    if request.method == "GET":
        countries = countriesController.get_everything()
        data_user = usersModel.show_id(managerData.email_to_id())
        
        data_render = {
            "image_profile" : managerData.image_name_saved_cookie_or_session(),
            "level_user_context" : managerData.level_saved_cookie_or_session(),
            "data_user" : data_user,
            "countries" : countries,
        }
    
        return render_template("home/admin/edit_profile.html", **data_render)
    else:
        data_update = {}
        data_update["user_name"] = request.form.get("user_name")
        data_update["user_surnames"] = request.form.get("user_surnames")
        data_update["user_email"] = request.form.get("user_email")
        data_update["user_number"] = request.form.get("user_number")
        res_image = uploadFiles.uploadFile(request.files.get("user_image"), PATH_UPLOAD_IMAGES_USERS)
        if res_image:
            session["user_profile_image"] = res_image
            data_update["user_image"] = res_image
        if request.form.get("new_password"):
            data_update["user_image"] = request.form.get("new_password")
        usersModel.user_update(managerData.email_to_id_admin(), data_update)

        flash("Se ha actualizado los datos.", "ok")
        return redirect(url_for("restaurant.editUserAdmin_1"))    

@restaurant.route("/edit_user_admin/2", methods = ["GET","POST"])
def editUserAdmin_2():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    if request.method == "GET":
        data_user = usersModel.show_id(managerData.email_to_id())
        
        data_render = {
            "image_profile" : managerData.image_name_saved_cookie_or_session(),
            "level_user_context" : managerData.level_saved_cookie_or_session(),
            "data_user" : data_user,
        }
    
        return render_template("home/admin/edit_profile_2.html", **data_render)
    
    else:
        data_update = {}
        data_for_qr = {}
        data_update["company_name"] = request.form.get("company_name")
        data_for_qr["company_name"] = request.form.get("company_name")
        data_update["company_description"] = request.form.get("company_description")
            
        data_update["company_location_1"] = request.form.get("company_location_1")
        data_update["company_location_2"] = request.form.get("company_location_2")
        data_update["company_location_3"] = request.form.get("company_location_3")
        data_update["company_location_4"] = request.form.get("company_location_4")
        data_update["company_location_coord"] = request.form.get("company_location_coord")
        res_image_company = uploadFiles.uploadFile(request.files.get("company_image"), PATH_UPLOAD_IMAGES_USERS)
        res_icon_company = uploadFiles.uploadFile(request.files.get("company_icon"), PATH_UPLOAD_ICONS_PARTNER)
        if res_image_company:
            data_update["company_image"] = res_image_company
        if res_icon_company:
            data_update["company_icon"] = res_icon_company
            data_for_qr["company_icon"] = res_icon_company
        else:
            data_for_qr["company_icon"] = request.form.get("current_company_icon")

        if ((request.form.get("id_secondary") != request.form.get("current_id_secondary")) or (data_update["company_name"] != request.form.get("current_company_name")) or res_icon_company ):
            data_for_qr["is"] = request.form.get("id_secondary").lower()
            data_update["id_secondary"] = request.form.get("id_secondary").lower()
            name_qr_code = "qr_code"+ str(managerData.email_to_id_admin()) +managerData.generate_random_letter()+".png"
            res_qr = qr_code_generator(str(data_for_qr), name_qr_code, PATH_UPLOAD_QR_CODE)
            data_update["qr_code_image"] = res_qr

        usersModel.user_update(managerData.email_to_id_admin(), data_update)
        flash("Se ha actualizado los datos.", "ok")
        return redirect(url_for("restaurant.editUserAdmin_2"))

@restaurant.route("/edit_user_admin/3", methods = ["GET","POST"])
def editUserAdmin_3():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    if request.method == "GET":
        data_user = usersModel.show_id(managerData.email_to_id())
        
        data_render = {
            "image_profile" : managerData.image_name_saved_cookie_or_session(),
            "level_user_context" : managerData.level_saved_cookie_or_session(),
            "data_user" : data_user,
        }
    
        return render_template("home/admin/edit_profile_3.html", **data_render)
    else:
        data_update = {}
        data_update["cash_payment_status"] = 1 if request.form.get("cash_payment_status") else 0
        data_update["yape_payment_status"] = 1 if request.form.get("yape_payment_status") else 0
        data_update["izipayya_payment_status"] = 1 if request.form.get("izipayya_payment_status") else 0
        data_update["bizum_payment_status"] = 1 if request.form.get("bizum_payment_status") else 0
            
        yape_payment_image = uploadFiles.uploadFile(request.files.get("yape_payment_image"), PATH_UPLOAD_IMAGE_PAY_METHODS)
        izipayya_payment_image = uploadFiles.uploadFile(request.files.get("izipayya_payment_image"), PATH_UPLOAD_IMAGE_PAY_METHODS)
        bizum_payment_image = uploadFiles.uploadFile(request.files.get("bizum_payment_image"), PATH_UPLOAD_IMAGE_PAY_METHODS)
        if yape_payment_image:
            data_update["yape_payment_image"] = yape_payment_image
        if izipayya_payment_image:
            data_update["izipayya_payment_image"] = izipayya_payment_image
        if bizum_payment_image:
            data_update["bizum_payment_image"] = bizum_payment_image

        usersModel.user_update(managerData.email_to_id_admin(), data_update)
        flash("Se ha actualizado los datos.", "ok")
        return redirect(url_for("restaurant.editUserAdmin_3"))

@restaurant.route("/edit_user_admin/4", methods = ["GET","POST"])
def editUserAdmin_4():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    if request.method == "GET":
        data_user = usersModel.show_id(managerData.email_to_id())
        data_config = configurationDataController.read({"id_admin":managerData.email_to_id_admin()})
        data_render = {
            "image_profile" : managerData.image_name_saved_cookie_or_session(),
            "level_user_context" : managerData.level_saved_cookie_or_session(),
            "data_user" : data_user,
            "data_config":data_config[0],
        }
    
        return render_template("home/admin/edit_profile_4.html", **data_render)
    else:
        data_update = {}
        data_update["email"] = request.form.get("email")
        data_update["password_email"] = request.form.get("password_email")
        data_update["language"] = request.form.get("language")
        data_update["currency"] = request.form.get("currency")
        data_update["time_zone"] = request.form.get("time_zone")
        data_update["order_now"] = request.form.get("order_now")
        data_update["reservations_accept"] = request.form.get("reservations_accept")
        data_update["delivery_accept"] = request.form.get("delivery_accept")
        data_update["visibility_in_app"] = request.form.get("visibility_in_app")
        data_update["send_email_1"] = request.form.get("send_email_1")
        data_update["send_email_2"] = request.form.get("send_email_2")
        data_update["maximum_distance_range"] = request.form.get("maximum_distance_range")
        data_update["price_per_delivery"] = request.form.get("price_per_delivery")
        configurationDataController.update(data_update)

        flash("Se ha actualizado los datos.", "ok")
        return redirect(url_for("restaurant.editUserAdmin_4"))

@restaurant.route("/edit_user_w", methods = ["GET", "POST"])
def userView():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    data_user = waitressModel.show_id_free(managerData.email_to_id())
    if request.method == "GET":
        data_render = {
                "image_profile" : managerData.image_name_saved_cookie_or_session(),
                "level_user_context" : managerData.level_saved_cookie_or_session(),
                "data_user" : data_user,
            }
        return render_template("home/users/edit_profile.html", **data_render)
    elif request.method == "POST":
        data_update = {"id_waitress":managerData.email_to_id()}
        data_update["user_first_name"] = request.form.get("user_first_name")
        data_update["user_last_name"] = request.form.get("user_last_name")
        data_update["user_email"] = request.form.get("user_email")
        data_update["user_phone_number"] = request.form.get("user_phone_number")
        if request.form.get("user_new_password"):
            data_update["user_password"] = request.form.get("user_new_password")
        image = uploadFiles.uploadFile(request.files.get("user_image"), PATH_UPLOAD_IMAGES_USERS)
        
        session["user_email"] = request.form.get("user_email")
        
        if image:
            data_update["user_image"] = image
            session["user_profile_image"] = image
        
        waitressModel.waitress_update_free(data_update)
        flash("Se actualizó los datos de usuario.", "ok")
        return redirect(url_for("restaurant.userView"))
    
@restaurant.route("/user/get", methods = ["get"])
def userGet():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    id = request.args.get("i")
    data = waitressModel.show_all({"id":id})
    if data:
        data_json = data[0].__dict__
        del(data_json["_sa_instance_state"])
        return data_json
    else:
        return {}

@restaurant.route("/user/create", methods = ["POST"])
def userCreate():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    user_role_ = request.form.get("user_role")
    names_ = request.form.get("names")
    surnames_ = request.form.get("surnames")
    email_ = request.form.get("email")
    telephone_ = request.form.get("telephone")
    password_ = request.form.get("password")
    image = uploadFiles.uploadFile(request.files.get("user_image"), PATH_UPLOAD_IMAGES_USERS)
    if image:
        images_profile = image
    else:
        images_profile = "/static/images/images_restaurant/images_profiles/default-avatar-profile-icon.jpg"
        
    status = waitressModel.waitress_insert(
        user_role = user_role_,
        first_name = names_,
        last_name = surnames_,
        phone_number = telephone_,
        email = email_,
        password = password_,
        image = images_profile,
        partner_id = managerData.email_to_id_admin(),
        box_id = 0,
    )
    return redirect(url_for("restaurant.waitressViewAccion"))

@restaurant.route("/user/update", methods = ["POST"])
def userEdit():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    form_data = dict(request.form)
    form_data["id_admin"] = managerData.email_to_id_admin()
    image = uploadFiles.uploadFile(request.files.get("user_image_update"), PATH_UPLOAD_IMAGES_USERS)
    if image:
        form_data["user_image"] = image
    waitressModel.waitress_update(form_data)
    return {}

@restaurant.route("/user/delete", methods = ["GET"])
def userDelete():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    id = request.args.get("i")
    waitressModel.waitress_delete({
        "id": id,
        "id_admin":managerData.email_to_id_admin(),
    })
    return {}

@restaurant.route("/panel", methods = ["GET", "POST"])
def reportAll(): 
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    
    if request.method == "GET":
        user_level = managerData.level_saved_cookie_or_session()
        email_to_id_admin = managerData.email_to_id_admin()
        dataBox = restaurantBoxController.get_all({"id_admin":email_to_id_admin})
        if not dataBox:
            restaurantBoxController.create({"id_admin":email_to_id_admin,"id_user" : 0,"total_amount_order" : 0,"daily_amount_order" : 0,"total_amount_reservation": 0,"daily_amount_reservation" : 0,"state" : 1,})
            dataBox = restaurantBoxController.get_all({"id_admin":email_to_id_admin})

        dataConfigAdmin = configurationDataController.read({"id_admin":email_to_id_admin})
        if not dataConfigAdmin:
            dataConfigAdmin = configurationDataController.insert({"id_admin":email_to_id_admin, "time_zone":"America/Lima"})
        else:
            dataConfigAdmin = dataConfigAdmin[0]
        
        data_order = orderModel.get_all_free({"id_user_context":email_to_id_admin, "user_level":managerData.level_saved_cookie_or_session(), "state_order":4})
        coworkers = [] #waitressModel.show_all({"partner_id":email_to_id_admin})
        
        zona_horaria_utc = pytz.timezone(dataConfigAdmin.time_zone)
        fecha_actual_utc = datetime.datetime.now(zona_horaria_utc)
        fecha_sin_hora = fecha_actual_utc.strftime('%Y-%m-%d')
        
        history =  recordModel.show_filter({"id_user_admin": email_to_id_admin ,"date_start":fecha_sin_hora})
        quantity_users = len(waitressModel.show_all({"partner_id": email_to_id_admin}))
        quantity_categories = len(typeFoodModel.show_all_free({"id_admin": email_to_id_admin}))
        quantity_foods = len(foodModel.show_all_free({"id_admin": email_to_id_admin}))
        data_user = managerData.data_user_context()
        if "partner_id" in data_user.keys():
            res_admin = usersModel.show_id(data_user["partner_id"])
            data_user["admin_data"] = res_admin
        if "subscription_end_date" in data_user and "subscription_end_date" in data_user:
            if data_user["subscription_start_date"] is not None:
                data_user["subscription_start_date"] = data_user["subscription_start_date"].strftime("%d-%m-%Y")
            if data_user["subscription_end_date"] is not None:
                data_user["subscription_end_date"] = data_user["subscription_end_date"].strftime("%d-%m-%Y")

        data_render = {
            "image_profile" : managerData.image_name_saved_cookie_or_session(),
            "level_user_context" : user_level,
            "current_history" : history,
            "data_box" : dataBox[0],
            "quantity_users" : quantity_users,
            "quantity_categories" : quantity_categories,
            "quantity_foods" : quantity_foods,   
            "quantity_order" : len(data_order),
            "coworkers":coworkers,
            "dataConfigAdmin": dataConfigAdmin,
        }
        if user_level == "2":
            return render_template("home/home_main.html", **data_render, **data_user)
        elif user_level == "4":
            return render_template("home/home_waiters.html", **data_render, **data_user)
        
    elif request.method == "POST":
        
        # amountModel.update_collect_main()
        return redirect(url_for("restaurant.reportAll"))
    
@restaurant.route("/ordenes")
def index():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    state_get = request.args.get("s")
    date_start = request.args.get("ds")
    date_end = request.args.get("de")
    if state_get in ["1", "2", "3", "5", "6"]:
        state_get_f = [21, 22] if state_get == "2" else state_get
        dfilter_order = {"id_user_admin":managerData.email_to_id_admin(), "state_order":state_get_f}
        if date_start: dfilter_order["date_start"] = date_start
        if date_end: dfilter_order["date_end"] = date_end
        
        order_table = orderModel.get_all_free(dfilter_order)
        tables = tableController.read({"id_admin":managerData.email_to_id_admin()})
        category_table = tableCategoryController.read({"id_admin":managerData.email_to_id_admin()})
        for order in order_table:
            order_with_product_code = False
            tablei = tableController.read({"id_admin":managerData.email_to_id_admin(), "id":order.id_table})
            if tablei:
                order.category_name = tablei[0].category_name
                order.number_table = tablei[0].number_table
                id_user = order.id_user_context
                user_level = order.user_level
                order.total_cost = 0
                if user_level == 2:
                    user_data = usersModel.show_all({"id_admin":id_user})
                    if user_data: order.user_context_name = user_data[0]["user_name"]+", "+user_data[0]["user_surnames"]
                elif user_level == 4:
                    user_data = waitressModel.show_all({"id":id_user})
                    if user_data: order.user_context_name = user_data[0].user_first_name+", "+user_data[0].user_last_name
                elif user_level == 5:
                    user_data = userAppController.read({"id":id_user})
                    if user_data: order.user_context_name = user_data[0]["first_name"]+", "+user_data[0]["last_name"]
                elif user_level == 6:
                    user_data = freeUserController.read({"id":id_user})
                    if user_data: order.user_context_name = user_data[0].name
                for d in order.data_orders:
                    food_data = foodModel.show_all_free({"id_food":d.id_food})
                    if food_data:
                        d.product_code = food_data[0]["product_code"]
                        d.food_name = food_data[0]["name"]
                        d.price = food_data[0]["price"]
                        d.image_food = food_data[0]["image"]
                        id_category = food_data[0]["type_food"]
                        cat_data = typeFoodModel.show_all_free({"id_type_food":id_category})
                        d.category_name = cat_data[0]["name_type"]
                        order.total_cost = order.total_cost + (float(d.price) * int(d.quantity))
                        if not order_with_product_code and food_data[0]["product_code"]:
                            order_with_product_code = True
                    d.observations = d.observation.split("///")
            order.order_with_product_code = order_with_product_code

        admin_data = usersModel.show_all({"id_admin": managerData.email_to_id_admin()})
        data_render = {
            "type_food_data" : typeFoodModel.show_all(),
            "image_profile" : managerData.image_name_saved_cookie_or_session(),
            "level_user_context" : managerData.level_saved_cookie_or_session(),
            "orderData" :order_table,
            "admin_data" : admin_data[0] if admin_data else {},
            "tables" : tables, 
            "category_table" : category_table,
            "s" : state_get,
        }
        if state_get == "1":
            return render_template("home/order.html", **data_render)
        elif state_get == "2":        
            return render_template("home/order_in_kitchen.html", **data_render)
        elif state_get == "3":        
            return render_template("home/order_in_table.html", **data_render)
        elif state_get == "5":
            return render_template("home/order_completed.html", **data_render)
        elif state_get == "6":
            return render_template("home/order_rejected.html", **data_render)
        else:
            return {"state" : "not found"}
    else:
        return {"state" : "not found"}
@restaurant.route("/ordenes/get_data_json")
def getDataOrder():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    id = request.args.get("id")
    if id:
        order = orderModel.get_all_free({"id_user_admin":managerData.email_to_id_admin(),"id":id})[0]
        data_table = tableController.read({"id_admin":managerData.email_to_id_admin(), "id":order.id_table})
        if data_table:
            order.number_table = data_table[0].number_table
            category_table_data = tableCategoryController.read({"id":data_table[0].category_id})
            order.category_table = category_table_data[0].name
            id_user = order.id_user_context
            user_level = order.user_level
            order.total_cost = 0
            if user_level == 2:
                user_data = usersModel.show_all({"id_admin":id_user})
                if user_data: order.user_context_name = user_data[0]["user_name"]+", "+user_data[0]["user_surnames"]
            elif user_level == 4:
                user_data = waitressModel.show_all({"id":id_user})
                if user_data: order.user_context_name = user_data[0].user_first_name+", "+user_data[0].user_last_name
            elif user_level == 5:
                user_data = userAppController.read({"id":id_user})
                if user_data: order.user_context_name = user_data[0]["first_name"]+", "+user_data[0]["last_name"]
            for d in order.data_orders:
                food_data = foodModel.show_all_free({"id_food":d.id_food})
                if food_data:
                    d.food_name = food_data[0]["name"]
                    d.price = food_data[0]["price"]
                    d.image_food = food_data[0]["image"]
                    id_category = food_data[0]["type_food"]
                    cat_data = typeFoodModel.show_all_free({"id_type_food":id_category})
                    d.category_name = cat_data[0]["name_type"]
                    order.total_cost = order.total_cost + (float(d.price) * int(d.quantity))
                d.observations = d.observation.split("///")

        list_data_orders = []
        for food in order.data_orders:
            temp_l = food.__dict__
            temp_l["observations"] = temp_l["observation"].split("///")
            del(temp_l["_sa_instance_state"])
            list_data_orders.append(temp_l)
        order = order.__dict__
        order["data_orders"] = list_data_orders
        del(order["_sa_instance_state"])
        return order
    else:
        return {}
@restaurant.route("/ordenes/get_quantity")
def getQuantityOrder():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    response_order = orderModel.get_all_free({"id_user_admin":managerData.email_to_id_admin(), "state_order" : [1, 2]})    
    ids = []
    for d in response_order:
        ids.append(d.id)
    return {"list_id": ids, "quantity":str(len(response_order))}

@restaurant.route("/datafoodmain/<string:obj>")
def datatypefood(obj):
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    id_admin = managerData.email_to_id_admin()
    configDataAdmin = configurationDataController.read({"id_admin":id_admin})
    if obj == "all":
        data = foodModel.show_all_free({"id_admin" : managerData.email_to_id_admin()})
        return {"data":data}
    else:
        data = foodModel.show_all_free({"id_admin" : managerData.email_to_id_admin(), "id_type_food" : obj})
        for d in data:
            d["currency"] = configDataAdmin[0].currency
        return {"data":data}

@restaurant.route("/create", methods=["GET", "POST"])
def dataCreate():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    
    if request.method == "GET":
        id_admin = managerData.email_to_id_admin()
        message = request.args.get("s")
        data_type_food = typeFoodModel.show_all()
        data_table = tableController.read({"id_admin":id_admin})
        data_categories_table = tableCategoryController.read({"id_admin":id_admin})
        data_order_info = orderModel.get_all_free({"id_user_admin":id_admin, "state_order":[21, 22]})
        data_order_process = {"orders_in_preparation":0, "orders_in_queue":0, "estimated_time":0}
        for d in data_order_info:
            if d.state_order == 21:
                data_order_process["orders_in_queue"] += 1
            elif d.state_order == 22:
                data_order_process["orders_in_preparation"] += 1
            for do in d.data_orders:
                id_food = do.id_food
                data_food = foodModel.show_all_free({"id":id_food})
                if data_food:
                    data_order_process["estimated_time"] = data_order_process["estimated_time"] + data_food[0]["preparation_time"]
        
        data_render = {
            "image_profile" : managerData.image_name_saved_cookie_or_session(),
            "level_user_context" : managerData.level_saved_cookie_or_session(),
            "message" : message,
            "data_type_food" : data_type_food,
            "data_table" : data_table,
            "data_categories_table": data_categories_table,
            "data_order_process" : data_order_process,
        }
        return render_template("home/create.html", **data_render)
        
@restaurant.route("/createfood", methods = ["POST"])
def dataCreateFood():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    incomingMethod=request.method
    if incomingMethod == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        price = request.form.get("price")
        preparation_time = request.form.get("preparation_time")
        product_code = request.form.get("product_code")
        type_food = request.form.get("type_food")
        filename = request.form.get("image")
        
        foodModel.insert(
            name=name,
            description=description,
            type_food = type_food,
            price = price,
            preparation_time = preparation_time,
            product_code = product_code,
            image = filename,
            state = 1,
        )
        
        return redirect( url_for("restaurant.dataShowFood", s=type_food))

@restaurant.route("/viewfoods")
def dataShowFood():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    user_level = managerData.level_saved_cookie_or_session()
    identifier_folder = request.args.get("s") if request.args.get("s") else 0
    data_full = []
    response = foodModel.show_all_free({
        "id_type_food" : identifier_folder,
    }) 
    message= request.args.get("s")
    for i in response:
        
        response_type = typeFoodModel.show_id(i["type_food"])
        if len(response_type) > 0:
            i["name_type"]=response_type["name_type"]
            data_full.append(i)

    data_type_food = typeFoodModel.show_all_free({
        "id_admin" : managerData.email_to_id_admin(),
        "id_type_food" : identifier_folder,
    })
    if len(data_type_food)<= 0:
        return redirect(url_for("restaurant.dbTypeFoodView"))
    dataConfigAdmin = configurationDataController.read({"id_admin":managerData.email_to_id_admin()})
    data_render = {
        "image_profile" : managerData.image_name_saved_cookie_or_session(),
        "dataFood" : data_full,
        "type_food_data" : data_type_food[0],
        "message" : message,
        "level_user_context" : user_level,
        "dataConfigAdmin" : dataConfigAdmin[0],
    }
    return render_template("home/view_food.html", **data_render)

@restaurant.route("/updatefoods", methods=["GET", "POST"])
def dataUpdateFood():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    
    if request.method == "GET":
        if request.args.get("row"):
            response = foodModel.show_id(request.args.get("row"))
            return response
        else:
            return {}
    
    elif request.method == "POST":
        id = request.form.get("row")
        if id:
            name = request.form.get("name")
            description = request.form.get("description")
            type_food = request.form.get("type_food")
            price = request.form.get("price")
            preparation_time = request.form.get("preparation_time")
            product_code = request.form.get("product_code")
            state = request.form.get("state")
            image = request.form.get("image")
            
            data = {}
            if name:
                data["name"] = name
            if description is not None:
                if description or len(description) == 0:
                    data["description"] = description
            if type_food:
                data["type_food"] = type_food
            if price:
                data["price"] = price
            if preparation_time:
                data["preparation_time"] = preparation_time
                
            data["product_code"] = product_code
            if state:
                data["state"] = state
            if image:
                data["image"] = image
            
            response_info = foodModel.update(id, data)
            return("ok")
        else:
            return False


@restaurant.route("/update", methods=["GET", "POST"])
def dataUpdate():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    user_level = managerData.level_saved_cookie_or_session()
    if request.method == "GET":
        id_row = request.args.get("row")
        if id_row:
            response = orderModel.show_id(id_row)
            return response
        
        else:
            return {}
        
    elif request.method == "POST":
        id_row = request.form.get("id_row")
        name = request.form.get("name")
        type_food = request.form.get("type_food")
        extras_food = request.form.get("extras_food")
        quantity_food = request.form.get("quantity_food")
        table_number = request.form.get("table_number")
        class_food = request.form.get("class_food")
        
        if id_row:
            response_update = orderModel.update(id_row,{
                "name" : name,
                "type_food" : type_food,
                "extras_food" : extras_food,
                "quantity_food" : quantity_food,
                "table_number" : table_number,
                "class_food" : class_food,
            })
            return "ok"
        else:
            return "error"

# DATA DB
@restaurant.route("/order/create_order", methods=["POST"])
def createOrder():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    id_admin = managerData.email_to_id_admin()
    if request.is_json:
        try:
            data = request.get_json()
            data_json_order = data[0]
            data_json_table = data[1]
            data_table = tableController.read({"number_table":data_json_table["number_table"], "id_admin": id_admin})
            if data_table:
                id_table = data_table[0].id
                d1 = {"state_order": 1, "id_user_admin": id_admin, "id_user_context":managerData.email_to_id(), "order_code":"", "user_level":managerData.level_saved_cookie_or_session(),"id_table":id_table}
                d1r = orderModel.insert(d1)
                for i in data_json_order:
                    for f in i["data"]:
                        d2 = {"id_admin":id_admin, "id_food": f["food_id"], "quantity":f["cantity"], "observation":"///".join(f["observations"]), "order_dishes_id":d1r.id, "type_order":f["category_order"]}
                        dataOrderController.insert(d2)
                order_code = str(d1r.id)+str(d1r.id_table)
                orderModel.update(d1r.id, {"id_admin" : id_admin,"order_code":order_code})
                tableController.update(id_table, {"state":2, "id_admin": id_admin})
                flash("Se ha enviado correctamente la orden.", "ok")
                recordModel.insert_record(order_code = order_code, added_amount = "Ninguno",movement_created = "Orden creada",description_action = "El usuario creó una orden.",)
                return str(d1r.id)
            else:
                flash("Error al enviar la orden. Número de mesa incorrecto.", "warning")    
                return "err"
        except Exception as err:
            flash("Error al enviar la orden.", "warning")
            print("Error al crear una orden------------------------------------", err)
            return "err"
    else:
        return "err"

@restaurant.route("/order/process_order_concluded", methods=["post"])
def processOrder():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    id_admin = managerData.email_to_id_admin()
    form_dict = dict(request.form)
    data_prepared = {"amt_1": None, "amt_2": None, "amt_3": None, "amt_4": None, "amt_5": None, "amt_6": None}
    data_prepared["id_admin"] = id_admin
    amount_to_add = 0
    if form_dict["pay-method-1"]:
        data_prepared["amt_1"] = form_dict["pay-method-1"]
        amount_to_add += float(form_dict["pay-method-1"])
    if form_dict["pay-method-2"]:data_prepared["amt_2"] = form_dict["pay-method-2"]
    if form_dict["pay-method-3"]:data_prepared["amt_3"] = form_dict["pay-method-3"]
    if form_dict["pay-method-4"]:data_prepared["amt_4"] = form_dict["pay-method-4"]
    if form_dict["pay-method-5"]:data_prepared["amt_5"] = form_dict["pay-method-5"]
    if form_dict["pay-method-6"]:data_prepared["amt_6"] = form_dict["pay-method-6"]

    resmb = mainBoxRestaurantController.read({"id_admin":id_admin})
    if resmb:
        resmb = resmb[0]
        amount_update_r = float(resmb.current_amount) + float(amount_to_add)
        if resmb.box_status == 1:
            mainBoxRestaurantController.update(id_admin, {"current_amount":amount_update_r})
        else:
            user_id = managerData.email_to_id()
            user_level = managerData.level_saved_cookie_or_session()
            mainBoxRestaurantController.update(id_admin, {"current_amount":amount_update_r, "box_status":1, "opened_by_id":user_id, "opened_by_level":user_level})
    else:
        pass
    data_prepared["order_or_table_id"] = form_dict["identifier"] if form_dict["identifier"] else form_dict["table_id"]
    data_prepared["mode"] = form_dict["mode"]
    res1 = paymentOrderController.insert(data_prepared)
    resemail = freeUserController.read({"id_admin":id_admin, "email":form_dict["email"]})
    if not resemail and form_dict["email"] and form_dict["name"]:
        res2 = freeUserController.insert({
            "user_level" : 7,
            "id_admin" :id_admin,
            "name" : form_dict["name"],
            "phone_number" : form_dict["phone_number"],
            "email" : form_dict["email"],
            "address" : form_dict["address"],
        })

    return form_dict

@restaurant.route("/freeuser/read", methods=["get"])
def usersFreeUser():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    id_admin = managerData.email_to_id_admin()
    email = request.args.get("email")
    res = freeUserController.read({"email":email, "id_admin":id_admin})
    if res:
        res = res[0].__dict__
        del(res["_sa_instance_state"])
        del(res["id"])
        del(res["id_admin"])

    return res

@restaurant.route("/order/delete", methods=["POST", "GET"])
def dbDelete():
    id_admin = managerData.email_to_id_admin()
    if not managerData.logged_user(): 
        # return redirect(url_for("pages.loginApp"))
        return "No logged"
    else:
        id_row = request.args.get("row")
        reso = orderModel.update(id_row, {"id_admin": id_admin, "state_order":6})
        recordModel.insert_record(order_code = reso.order_code, added_amount = "Ninguno",movement_created = "Orden rechazada",description_action = "El usuario rechazó una órden de la seccion de órdenes",)
        return "ok"

@restaurant.route("/update_order_state", methods=["GET"])
def dbUpdateState():
    if not managerData.logged_user():
        return "error"
    else:
        id_row = request.args.get("row")
        new_state = request.args.get("state")
        response = orderModel.get_all_free({"id":id_row, "id_user_admin":managerData.email_to_id_admin()})
        resp_box_data = restaurantBoxController.get_all({"id_admin": managerData.email_to_id_admin()})
        order_code = response[0].order_code
        id_box = resp_box_data[0]["id"]
        amount_all_temp = 0
        if int(new_state) == 5:
            for f in response[0].data_orders:
                id_food = f.id_food
                resf = foodModel.show_all_free({"id":id_food})
                price = resf[0]["price"]
                product_code = resf[0]["product_code"]
                if product_code:
                    resi = inventoryController.get_all_free({"product_code":product_code, "id_admin":managerData.email_to_id_admin()})
                    if resi:
                        data_for_sales = {}
                        data_for_sales["id_admin"] = managerData.email_to_id_admin()
                        data_for_sales["id_product"] = resi[0].id
                        data_for_sales["customer"] = "ORDEN=["+ response[0].order_code +"]"
                        data_for_sales["quantity"] = f.quantity
                        data_for_sales["discount"] = 0
                        data_for_sales["pay_method"] = 4
                        data_for_sales["amount_unsettled"] = 0
                        data_for_sales["amount_due"] = 0
                        data_for_sales["amount_paid"] = f.quantity * resi[0].sale_price
                        data_for_sales["state"] = 1
                        salesInventoryController.insert(data_for_sales)
                        inventoryController.update(resi[0].id, {"id_admin":managerData.email_to_id_admin(), "quantity":resi[0].quantity - f.quantity})
                
                total_price = int(f.quantity) * float(price)
                amount_all_temp += total_price

            new_daily_amount_reservation = float(resp_box_data[0]["daily_amount_order"]) + amount_all_temp
            restaurantBoxController.update(id_box, {"daily_amount_order":new_daily_amount_reservation})

            id_user = 0
            if managerData.level_saved_cookie_or_session() == 4:
                id_user = managerData.email_to_id()
            new_daily_quantity_reservation = int(resp_box_data[0]["daily_quantity_order"]) + 1
            restaurantBoxController.update(id_box, {"daily_quantity_order":new_daily_quantity_reservation, "id_user":id_user})
            recordModel.insert_record(order_code=order_code, added_amount = "Ninguno",movement_created = "Orden concluída",description_action = "El usuario concluyó la orden.",)
        elif int(new_state) == 2:
            recordModel.insert_record(order_code=order_code, added_amount = "Ninguno",movement_created = "Orden aceptado",description_action = "El usuario envió una orden a la cocina.",)
        elif int(new_state) == 3:
            recordModel.insert_record(order_code=order_code, added_amount = "Ninguno",movement_created = "Orden preparada",description_action = "El usuario entregó el orden al mesero(a).",)
        elif int(new_state) == 4:
            recordModel.insert_record(order_code=order_code, added_amount = "Ninguno",movement_created = "Orden entregado",description_action = "El usuario entregó el orden a la mesa correspondiente.",)
        orderModel.update_status(id_row, new_state)
        
        return "ok"
@restaurant.route("/update_order_state/complet_by_table", methods=["GET"])
def dbUpdateStateOrderByTable():
    if not managerData.logged_user():
        return "error"
    else:
        id_row = request.args.get("row")
        user_context_id = request.args.get("u")
        user_level = request.args.get("l")
        new_state = 5
        data_query_filter = {"id_table":id_row, "id_user_admin":managerData.email_to_id_admin(), "state_order":4}
        if user_context_id:
            data_query_filter["id_user_context"] = user_context_id
        if user_level:
            data_query_filter["user_level"] = user_level

        response = orderModel.get_all_free(data_query_filter)
        resp_box_data = restaurantBoxController.get_all({"id_admin": managerData.email_to_id_admin()})
        id_box = resp_box_data[0]["id"]
        amount_all_temp = 0
        quantity_all_temp = 0
        for i in response:
            for f in i.data_orders:
                id_food = f.id_food
                resf = foodModel.show_all_free({"id":id_food, "id_admin":managerData.email_to_id_admin()})
                price = resf[0]["price"]
                total_price = int(f.quantity) * float(price)
                amount_all_temp += total_price

                product_code = resf[0]["product_code"]
                if product_code:
                    resi = inventoryController.get_all_free({"product_code":product_code, "id_admin":managerData.email_to_id_admin()})
                    if resi:
                        data_for_sales = {}
                        data_for_sales["id_admin"] = managerData.email_to_id_admin()
                        data_for_sales["id_product"] = resi[0].id
                        data_for_sales["customer"] = "ORDEN=["+ response[0].order_code +"]"
                        data_for_sales["quantity"] = f.quantity
                        data_for_sales["discount"] = 0
                        data_for_sales["pay_method"] = 4
                        data_for_sales["amount_unsettled"] = 0
                        data_for_sales["amount_due"] = 0
                        data_for_sales["amount_paid"] = f.quantity * resi[0].sale_price
                        data_for_sales["state"] = 1
                        salesInventoryController.insert(data_for_sales)
                        inventoryController.update(resi[0].id, {"id_admin":managerData.email_to_id_admin(), "quantity":resi[0].quantity - f.quantity})
                
            orderModel.update_status(i.id, new_state)
            quantity_all_temp += 1

        new_daily_amount_reservation = float(resp_box_data[0]["daily_amount_order"]) + amount_all_temp
        restaurantBoxController.update(id_box, {"daily_amount_order":new_daily_amount_reservation})

        id_user = 0
        if managerData.level_saved_cookie_or_session() == 4:
            id_user = managerData.email_to_id()
        new_daily_quantity_reservation = int(resp_box_data[0]["daily_quantity_order"]) + quantity_all_temp
        restaurantBoxController.update(id_box, {"daily_quantity_order":new_daily_quantity_reservation, "id_user":id_user})
        flash("Se concluyó los órdenes correctamente.", "ok")
        return "ok"

@restaurant.route("/order/update/table", methods=["POST"])
def update_table_order():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    id_admin = managerData.email_to_id_admin()
    data_json = request.get_json()
    if "id_table" in data_json.keys():
        order_id = data_json["order_id"]
        table_id = data_json["id_table"]
        res1 = orderModel.update(order_id, {"id_admin":id_admin, "id_table" : table_id})
        res2 = tableController.update(table_id, {"id_admin" : id_admin, "state":2})
        return {"state" : "ok"}
    else:
        return {"state" : "error"}

@restaurant.route("/order/update/data_order", methods=["POST"])
def update_data_order():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    id_admin = managerData.email_to_id_admin()
    data = request.get_json()
    djson = {"id" : data["id_data_order"]}
    data_order = dataOrderController.read(djson)
    comments = []
    if data_order:
        comments = commentsFoodController.get_everything({"id_admin":id_admin, "id_type_food" : data_order[0]["category_id"]})
        return {"data_food" : data_order[0], "data_comments" : comments} 
    else:
        return {}

@restaurant.route("/order/update/data_order/update", methods=["POST"])
def update_data_order_update():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    id_admin = managerData.email_to_id_admin()
    id_data_order = request.form.get("id_data_order")
    comments = request.form.get("new_comment")
    quantity = request.form.get("new_quantity")
    type = request.form.get("new_type")

    res = dataOrderController.update(id_data_order, {"id_admin":id_admin, "quantity":quantity, "observation":comments, "type_order":type})
    flash("Se actualizaron correctamente", "ok")
    return {}


@restaurant.route("/delete_f_d", methods=["GET"])
def dbDeleteFoodDishes():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    id_row = request.args.get("row")
    response = foodModel.delete(id_row)
    flash("Se ha creado un plato correctamente.", "ok")
    return("ok")

@restaurant.route("/typefoodroute", methods=["GET"])
def dbTypeFoodView():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    user_level = managerData.level_saved_cookie_or_session()
    requestType = request.method
    status_delete = ""
    data_flased = get_flashed_messages()
    if data_flased:
        try:
            status_delete = data_flased[0]["status"]
        except Exception as error:
            print(error)
    data_all = typeFoodModel.show_all()
    data_render = {
        "image_profile" : managerData.image_name_saved_cookie_or_session(),
        "typeFoodData" : data_all,
        "status_delete" : status_delete,
        "level_user_context" : user_level,
    }
    return render_template("home/type_food_view.html", **data_render)

@restaurant.route("/typefoodabs", methods=["POST"])
def dbTypeFoodCreate():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    
    requestType = request.method
    if requestType =="POST":
        name_type = request.form.get("name_type")
        description = request.form.get("description")
        filename = request.form.get("image")
        typeFoodModel.insert(name_type=name_type,description=description , image= filename,state = 1)
        return("ok")
    

@restaurant.route("/typefoodabs_view", methods=["GET"])
def dbTypeFoodViewID():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    
    requestType = request.method
    if requestType =="GET":
        id = request.args.get("row")
        if (id):
            data = typeFoodModel.show_id(id)
            return(data)
        else:
            return({"status": "error"})


@restaurant.route("/typefoodroute_delete", methods=["GET"])
def dbTypeFoodDelete():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    
    id_row = request.args.get("row")
    res_ = typeFoodModel.delete(id_row)
    flash("Se ha eliminado una categoría correctamente.", "ok")
    return "ok"

@restaurant.route("/typefoodroute_update", methods=["POST"])
def dbTypeFoodUpdate():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    data = {}
    id_row = request.form.get("row")
    state = request.form.get("state")
    name_type = request.form.get("name_type")
    description = request.form.get("description")
    file = request.form.get("image")
    if state:
        data["state"] = state 
    if file:
        data["image"] = file
    if name_type:
        data["name_type"] = name_type
    if description is not None:
        if description or len(description) == 0:        
            data["description"] = description

    if len(data) > 0:
        res_ = typeFoodModel.update(id_row, data)
        flash("Se ha actualizado una categoría correctamente.", "ok")
        return "ok"
    else:
        flash("Ocurrió un error inesperado al actualizar una categoría.", "error")
        return "error"


@restaurant.route("/record_movements", methods=["GET"])
def recordMovements():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    id_admin = managerData.email_to_id_admin()
    user_info = request.args.get("waitress")    
    date_start = request.args.get("date_start")
    date_end = request.args.get("date_end")

    data_json_filter = {"id_user_admin":id_admin}
    if user_info:
        user_level = user_info.split("-")[0]
        waitress_id = user_info.split("-")[1]         
        data_json_filter["user_level"] = user_level
        data_json_filter["id_user_captured"] = waitress_id

    if date_start: data_json_filter["date_start"] = date_start
    if date_end: data_json_filter["date_end"] = date_end

    data = recordModel.show_filter(data_json_filter)

    data_admin = usersModel.show_all({"id_admin" : id_admin})
    waitress_all = waitressModel.show_all({"partner_id":id_admin})
    
    data_render = {
        "image_profile" : managerData.image_name_saved_cookie_or_session(),
        "level_user_context" : managerData.level_saved_cookie_or_session(),
        "waitress_data" : waitress_all,
        "data_admin" : data_admin[0],
        "data_record" : data,
    }
    return render_template("home/record_movements.html", **data_render)

@restaurant.route("/waitress/waitress_search", methods=["GET"])
def waitressSearchAccion():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    data = request.args.get("e")
    if data is not None:
        response = waitressModel.show_email(data)
        return response
    else:
        return {}

@restaurant.route("/waitress_view", methods=["GET", "POST"])
def waitressViewAccion():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    user_level = managerData.level_saved_cookie_or_session()
    partner_id = managerData.email_to_id_admin()
    data_waitress = waitressModel.show_all({"partner_id" : partner_id})
    
    message = request.args.get("s") 

    data_user = usersModel.show_id(managerData.email_to_id())
    
    data_render = {
        "image_profile" : managerData.image_name_saved_cookie_or_session(),
        "data_user" : data_user,
        "data_waitress" : data_waitress,
        "message" : message,
        "level_user_context" : user_level,
    }
    return render_template("home/waitress_view.html", **data_render)

@restaurant.route("/waitress/waitress_link_up", methods=["POST"])
def waitressLinkUpAccion():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    if request.method == "POST":
        id = request.form.get("id_user")
        if id:
            state = jobApplication_c.create({
                "id_user": id,
            })
            return  {"response" : state}
        else:
            return "error"
    else:
        return "Error"
        
        
@restaurant.route("/waitress_create", methods=["GET", "POST"])
def waitressCreateAccion():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    user_level = managerData.level_saved_cookie_or_session()
    if request.method == "GET":
        message = request.args.get("s")
        
        data_user = usersModel.show_id(managerData.email_to_id())
        
        # jobApplication_c.update_status({"status":1,"id_admin":True, "id_user":2})

        data_render = {
            "image_profile" : managerData.image_name_saved_cookie_or_session(),
            "data_user" : data_user,
            "message" : message,
            "level_user_context" : user_level,
        }
        return render_template("home/waitress_create.html", **data_render)
    
    elif request.method == "POST":
        
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        phone_number = request.form.get("phone_number")
        email = request.form.get("email")
        password = request.form.get("password") 
        image = request.form.get("image")
        name_image = "logo_food_13.png"
        if "image" in request.files:
            file = request.files.get("image")
            if len(name_image) > 0:
                name_image = file.filename
                extension = name_image.split(".")[-1]
                fecha_hora_actual = datetime.datetime.now()
                fecha_hora_formateada = fecha_hora_actual.strftime('%Y-%m-%d_%H_%M_%S')
                al = managerData.generate_random_letter(9)
                
                name_image =str(fecha_hora_formateada) + str(al)+"."+ str(extension)
                file.save(os.path.join(PATH_UPLOAD_IMAGES_USERS ,name_image))
                
        waitressModel.waitress_insert(
            first_name = first_name,
            last_name = last_name,
            phone_number = phone_number,
            email = email,
            password = password,
            image = name_image,
            
        )
        
        return redirect(url_for("restaurant.waitressCreateAccion", s = 200))

@restaurant.route("/waitress_update", methods=["GET", "POST"])
def waitressUpdateAccion():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    user_level = managerData.level_saved_cookie_or_session()
    if request.method == "GET":
        id_waitress = request.args.get("row")
        session["id_waitress_for_update"] = id_waitress
        response = waitressModel.show_id(id_waitress)
        
        data_user = usersModel.show_id(managerData.email_to_id())
        data_render = {
            "image_profile" : managerData.image_name_saved_cookie_or_session(),
            "data_user" : data_user,
            "data_waitress" : response,
            "level_user_context" : user_level,
        }
        return render_template("home/waitress_update.html", **data_render)
        
    
    elif request.method == "POST":
        
        p_c = request.form.get("p_c")
        p_u = request.form.get("p_u")
        p_d = request.form.get("p_d")
        p_s = request.form.get("p_s")
        
        if "id_waitress_for_update" in session:
            id_waitress = session["id_waitress_for_update"]
            
            response = waitressModel.waitress_update({
                "id_waitress" : id_waitress,
                "p_create_1" : p_c,
                "p_update_1" : p_u,
                "p_delete_1" : p_d,
                "p_confirm_1" : p_s,
            })
            return redirect(url_for("restaurant.waitressUpdateAccion", row=id_waitress))
                
        else:
            flash({"mesage": "Ocurrió un error"})
            return redirect(url_for("restaurant.waitressViewAccion"))
            
@restaurant.route("/waitress_delete", methods=["GET"])
def waitressDeleteAccion():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    
    id_waitress = request.args.get("row")
    response = waitressModel.waitress_delete(id=id_waitress)
    jobApplication_c.delete({"id_admin":True, "id_user":id_waitress})
    flash("Se desconectó del administrador.", "ok")
    return "ok"



# Notificaciones
@restaurant.route("/notifications")
def notificationsAll():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    # probelam de ID con admin y users
    notifications = notificationsController.get_all({"id_receiver": managerData.email_to_id(), "level_receiver":managerData.level_saved_cookie_or_session(),"state":1})
    
    data_render = {
        "image_profile" : managerData.image_name_saved_cookie_or_session(),
        "level_user_context" : managerData.level_saved_cookie_or_session(),
        "notifications" : notifications,
    }
    return render_template("home/notifications.html", **data_render)

@restaurant.route("/notifications_users")
def notifications():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))

    data_main = []
    data_all = jobApplication_c.get_all()
    for data in data_all:
        dic_temp = {}
        # data_main.append
        data_admin = usersModel.show_id(data["id_admin"])
        dic_temp["id"] = data_admin["id"]
        dic_temp["admin_name"] = data_admin["user_name"]
        dic_temp["admin_surnames"] = data_admin["user_surnames"]
        dic_temp["admin_email"] = data_admin["user_email"]
        dic_temp["admin_number"] = data_admin["user_number"]
        dic_temp["admin_image"] = data_admin["user_image"]
        dic_temp["company_location"] = data_admin["company_location_2"] 
        dic_temp["company_description"] = data_admin["company_description"]
        dic_temp["company_image"] = data_admin["company_image"]
        dic_temp["company_name"] = data_admin["company_name"]

        data_main.append(dic_temp)
    notifications = notificationsController.get_all({"id_receiver": managerData.email_to_id(), "level_receiver":managerData.level_saved_cookie_or_session(),"state":1})
    for n in notifications:
        response = usersModel.show_all({"id_admin":n["id_sender"]})
        if response:
            n["data_sender"] = {"image_profile":response[0]["user_image"], "name_sender":response[0]["user_name"]+", "+response[0]["user_surnames"]}
    data_render = {
        "notifications" : notifications,
        "JobsApp" : data_main,
        "image_profile" : managerData.image_name_saved_cookie_or_session(),
        "level_user_context" : managerData.level_saved_cookie_or_session(),
    }
    return render_template("home/jobs/users/notifications.html", **data_render)
@restaurant.route("/notifications_users/delete")
def notification_delete():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    row = request.args.get("row")
    res = notificationsController.delete({"id" : row})
    
    return "ok"

@restaurant.route("/create-notifications", methods = ["GET", "POST"])
def createNotifications():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))

    if request.method == "GET":
        users = waitressModel.show_all()
        # notifications = notificationsController.get_all({"id_sender": managerData.email_to_id_admin(), "status":1})
        
        data_render = {
            "image_profile" : managerData.image_name_saved_cookie_or_session(),
            "level_user_context" : managerData.level_saved_cookie_or_session(),
            "users" : users,
            # "notifications" : notifications,
        }
        return render_template("home/admin/create_notifications.html", **data_render)
    elif request.method == "POST":
        flash("Se há enviado correctamente la notificación.", "ok")
        data_post = {
            "id_sender" : managerData.email_to_id_admin(), 
            "level_sender" : managerData.level_saved_cookie_or_session(), 
            "id_receiver" : request.form.get("id_receiver"),
            "level_receiver" : 4, 
            "title" : request.form.get("title"), 
            "text" : request.form.get("text"), 
            "link" : request.form.get("link"),
            }
        notificationsController.create(data_post)

        return redirect(url_for("restaurant.createNotifications"))

@restaurant.route("/waitress_linked_admin", methods=["POST"])
def waitresLinkedAdmin ():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))

    if request.method == "POST":
        id = request.form.get("id")
        status = request.form.get("status")
        if status:
            if int(status) == 0:
                jobApplication_c.update_status({"status":0, "id_admin":id})
            elif int(status) == 2:
                jobApplication_c.update_status({"status":2, "id_admin":id})
                waitressModel.update_partner_id({"id_admin":id})

    return "ok"


# Notificaciones fin
# REPORTS
@restaurant.route("/reports-admin")
def reports():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    if request.method == "GET":
        id_admin_m = managerData.email_to_id_admin()
        admin_info = usersModel.show_id(id_admin_m)   
        type_all = typeFoodModel.show_all_free({"id_admin" : id_admin_m})
        user_all = waitressModel.show_all({"partner_id":id_admin_m})
        del(admin_info["id"])

        mode_filter = request.args.get("mode_filter")
        user_w = request.args.get("user")
        category = request.args.get("category")
        date_start = request.args.get("date_start")
        date_end =  request.args.get("date_end")
        data_get_filter = {
            "mode_filter":mode_filter,
            "user":user_w,
            "category":category,
            "date_start":date_start,
            "date_end":date_end,
            }
        usuario = {}
        data_for_apexcharts = []
        if not mode_filter or int(mode_filter) == 1:
            d_order = []
            c_order = []
            keys_order_temp = []
            orders =  orderModel.get_all_free({"id_user_admin":id_admin_m, "state_order" : 5})
            # para plato
            for order in orders:
                for food in order.data_orders:
                    if food.id_food in keys_order_temp:
                        for do in d_order:
                            if do["identifier"] == food.id_food:
                                do["quantity_food"] += int(food.quantity)
                                break
                    else:
                        d_order.append({"identifier": food.id_food, "quantity_food":int(food.quantity)})
                        keys_order_temp.append(food.id_food)
            # categoria
            category_order_name_temp = []
            for order in d_order:
                food_response = foodModel.show_all_free({"id_food":order["identifier"]})
                if food_response:
                    food_name = food_response[0]["name"]
                    id_category = food_response[0]["type_food"]
                    category_response = typeFoodModel.show_all_free({"id_type_food":id_category})
                    if category_response:
                        category_name = category_response[0]["name_type"]
                        order["price"] = food_response[0]["price"]
                        order["total_price"] = float(food_response[0]["price"]) * int(order["quantity_food"])
                        order["food_name"] = food_name
                        order["category_name"] = category_name      
                        if category_name in category_order_name_temp:
                            for c in c_order:
                                if c["category_name"] == category_name:
                                    c["quantity_category"] += order["quantity_food"]
                                    c["amount_all"] += order["total_price"]
                                    break
                        else:
                            category_order_name_temp.append(category_name)
                            c_order.append({"quantity_category":order["quantity_food"], "category_name":category_name, "least_sold":None, "most_sold":None, "amount_all":order["total_price"]})
            for cp in c_order:
                category_min_max_temp = [{"quantity_food":None}, {"quantity_food":0}]
                for fp in d_order:
                    if cp["category_name"] == fp["category_name"]:
                        if category_min_max_temp[0]["quantity_food"]:
                            if int(fp["quantity_food"]) < category_min_max_temp[0]["quantity_food"]:
                                category_min_max_temp[0]["quantity_food"] = int(fp["quantity_food"])
                                category_min_max_temp[0]["food_name"] = fp["food_name"]
                        else:
                            category_min_max_temp[0]["quantity_food"] = int(fp["quantity_food"])
                            category_min_max_temp[0]["food_name"] = fp["food_name"]
                        if int(fp["quantity_food"]) > category_min_max_temp[1]["quantity_food"]:
                            category_min_max_temp[1]["quantity_food"] = int(fp["quantity_food"])
                            category_min_max_temp[1]["food_name"] = fp["food_name"]
                cp["least_sold"] = category_min_max_temp[0]["food_name"]
                cp["most_sold"] = category_min_max_temp[1]["food_name"]

            data_for_apexcharts = [d_order, c_order]
            
            # usuario
            
            for order in orders:
                order_id_user_context_level = str(order.id_user_context)+"-"+str(order.user_level)
                if order.user_level == 2:
                    user_data = usersModel.show_all({"id_admin": order.id_user_context})    
                    order.user_context_name = user_data[0]["user_name"]+", "+user_data[0]["user_surnames"]
                elif order.user_level == 4:
                    user_data = waitressModel.show_all({"id":order.id_user_context})
                    order.user_context_name = user_data[0].user_first_name+", "+user_data[0].user_last_name
                else:
                    order.user_context_name = "Usuario de neeva"

                if order_id_user_context_level not in usuario.keys():
                    usuario[order_id_user_context_level] = {"user_context_name":order.user_context_name,"category_foods":{},"most_sold_category":"", "number_of_categories":0, "foods":{},"most_sold_food":"" ,"number_of_foods":0, "amount_all":0}
                    for data in order.data_orders:
                        f_temp = foodModel.show_all_free({"id":data.id_food})
                        data.category_id = f_temp[0]["type_food"]
                        c_temp = typeFoodModel.show_all_free({"id_type_food":data.category_id})
                        data.category_name = c_temp[0]["name_type"]
                        
                        usuario[order_id_user_context_level]["number_of_categories"] = int(usuario[order_id_user_context_level]["number_of_categories"]) + 1
                        if data.category_id not in usuario[order_id_user_context_level]["category_foods"].keys():
                            usuario[order_id_user_context_level]["category_foods"][data.category_id] = {"name_type_food":data.category_name, "cantity":1}
                        else:
                            usuario[order_id_user_context_level]["category_foods"][data.category_id]["cantity"] = int(usuario[order_id_user_context_level]["category_foods"][data.category_id]["cantity"]) + 1
                        
                        usuario[order_id_user_context_level]["number_of_foods"] = int(usuario[order_id_user_context_level]["number_of_foods"]) + int(data.quantity)
                        usuario[order_id_user_context_level]["amount_all"] = float(usuario[order_id_user_context_level]["amount_all"]) + (float(f_temp[0]["price"]) * int(data.quantity))
                        if data.id_food not in usuario[order_id_user_context_level]["foods"].keys():
                            usuario[order_id_user_context_level]["foods"][data.id_food] = {"food_name":f_temp[0]["name"], "cantity":int(data.quantity)}
                        else:
                            usuario[order_id_user_context_level]["foods"][data.id_food]["cantity"] = int(usuario[order_id_user_context_level]["foods"][data.id_food]["cantity"]) + int(data.quantity)
                else:
                    for data in order.data_orders:
                        f_temp = foodModel.show_all_free({"id":data.id_food})
                        data.category_id = f_temp[0]["type_food"]
                        c_temp = typeFoodModel.show_all_free({"id_type_food":data.category_id})
                        data.category_name = c_temp[0]["name_type"]

                        usuario[order_id_user_context_level]["number_of_categories"] = int(usuario[order_id_user_context_level]["number_of_categories"]) + 1
                        if data.category_id not in usuario[order_id_user_context_level]["category_foods"].keys():
                            usuario[order_id_user_context_level]["category_foods"][data.category_id] = {"name_type_food":data.category_name, "cantity":1}
                        else:
                            usuario[order_id_user_context_level]["category_foods"][data.category_id]["cantity"] = int(usuario[order_id_user_context_level]["category_foods"][data.category_id]["cantity"]) + 1
                        
                        usuario[order_id_user_context_level]["number_of_foods"] = int(usuario[order_id_user_context_level]["number_of_foods"]) + int(data.quantity)
                        usuario[order_id_user_context_level]["amount_all"] = float(usuario[order_id_user_context_level]["amount_all"]) + (float(f_temp[0]["price"]) * int(data.quantity))
                        if data.id_food not in usuario[order_id_user_context_level]["foods"].keys():
                            usuario[order_id_user_context_level]["foods"][data.id_food] = {"food_name":f_temp[0]["name"], "cantity":int(data.quantity)}
                        else:
                            usuario[order_id_user_context_level]["foods"][data.id_food]["cantity"] = int(usuario[order_id_user_context_level]["foods"][data.id_food]["cantity"]) + int(data.quantity)

            for c in usuario:
                # food
                min_f = None
                min_f_t = ""
                max_f = None
                max_f_t = ""
                for f in usuario[c]["foods"]:
                    cant = usuario[c]["foods"][f]["cantity"]
                    nam = usuario[c]["foods"][f]["food_name"]
                    if min_f == None or min_f > int(cant):
                        min_f = int(cant)
                        min_f_t = nam
                    if max_f == None or max_f < int(cant):
                        max_f = int(cant)
                        max_f_t = nam
                usuario[c]["most_sold_food"] = max_f_t
                usuario[c]["least_sold_food"] = min_f_t
                # category
                min_c = None
                min_c_t = ""
                max_c = None
                max_c_t = ""
                for f in usuario[c]["category_foods"]:
                    cant = usuario[c]["category_foods"][f]["cantity"]
                    nam = usuario[c]["category_foods"][f]["name_type_food"]
                    if min_c == None or min_c > int(cant):
                        min_c = int(cant)
                        min_c_t = nam
                    if max_c == None or max_c < int(cant):
                        max_c = int(cant)
                        max_c_t = nam
                usuario[c]["most_sold_category"] = max_c_t
                usuario[c]["least_sold_category"] = min_c_t

        elif int(mode_filter) == 2:
            reservations = reservationsFoodsController.get_all({"id_admin":managerData.email_to_id_admin(), "only_state":3})
            d_reservation = []
            c_reservation = []
            keys_temp = []
            for r in reservations:
                foods_re = json.loads(r["foods_reservation"].replace("'", '"'))
                for f in foods_re:    
                    if f["identifier"] in keys_temp:
                        for d in d_reservation:
                            if d["identifier"] == f["identifier"]:
                                d["quantity_food"] += int(f["cantity"]) 
                                break
                    else:
                        d_reservation.append({"identifier": f["identifier"], "quantity_food":int(f["cantity"])})
                        keys_temp.append(f["identifier"])
            category_name_temp = []
            for m in d_reservation:
                food_response = foodModel.show_all_free({"id_food":m["identifier"]})
                if food_response:
                    food_name = food_response[0]["name"]
                    id_category = food_response[0]["type_food"]
                    category_response = typeFoodModel.show_all_free({"id_type_food":id_category})
                    if category_response:
                        category_name = category_response[0]["name_type"]
                        m["price"] = food_response[0]["price"]
                        m["total_price"] = float(food_response[0]["price"]) * int(m["quantity_food"])
                        m["food_name"] = food_name
                        m["category_name"] = category_name      
                        if category_name in category_name_temp:
                            for c in c_reservation:
                                if c["category_name"] == category_name:
                                    c["quantity_category"] += m["quantity_food"]
                                    c["amount_all"] += m["total_price"]
                                    break
                        else:
                            category_name_temp.append(category_name)
                            c_reservation.append({"quantity_category":m["quantity_food"], "category_name":category_name, "least_sold":None, "most_sold":None, "amount_all":m["total_price"]})
                                    

            for cp in c_reservation:
                category_min_max_temp = [{"quantity_food":None}, {"quantity_food":0}]
                for fp in d_reservation:
                    if cp["category_name"] == fp["category_name"]:
                        if category_min_max_temp[0]["quantity_food"]:
                            if int(fp["quantity_food"]) < category_min_max_temp[0]["quantity_food"]:
                                category_min_max_temp[0]["quantity_food"] = int(fp["quantity_food"])
                                category_min_max_temp[0]["food_name"] = fp["food_name"]
                        else:
                            category_min_max_temp[0]["quantity_food"] = int(fp["quantity_food"])
                            category_min_max_temp[0]["food_name"] = fp["food_name"]
                        if int(fp["quantity_food"]) > category_min_max_temp[1]["quantity_food"]:
                            category_min_max_temp[1]["quantity_food"] = int(fp["quantity_food"])
                            category_min_max_temp[1]["food_name"] = fp["food_name"]
                cp["least_sold"] = category_min_max_temp[0]["food_name"]
                cp["most_sold"] = category_min_max_temp[1]["food_name"]

            data_for_apexcharts = [d_reservation, c_reservation]
            
        data_render = {
                "image_profile" : managerData.image_name_saved_cookie_or_session(),
                "level_user_context" : managerData.level_saved_cookie_or_session(),
                "data_admin" :admin_info,                
                "type_all" : type_all,
                "user_all" : user_all,
                "data_table_1" : data_for_apexcharts[0],
                "data_table_2" : data_for_apexcharts[1], 
                "data_table_3" : usuario,
                "data_get" : data_get_filter
            }
        if request.args.get("for") == "apex":
            return [data_for_apexcharts]
        else:
            return render_template("home/admin/reports.html", **data_render)

# REPORTS FIN
# Observaciones food
@restaurant.route("/observations_foods", methods=["POST", "GET"])
def observations_food():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    if request.method == "GET":
        type_foods = typeFoodModel.show_all_free({"id_admin":managerData.email_to_id_admin()})
        comments_foods = commentsFoodController.get_everything({"id_admin":managerData.email_to_id_admin()})
        for cm in comments_foods:
            res_tfood = typeFoodModel.show_id(id = cm["id_type_food"])
            if res_tfood:
                cm["id_type_food"] = res_tfood["name_type"]

        
        data_render = {
            "image_profile" : managerData.image_name_saved_cookie_or_session(),
            "level_user_context" : managerData.level_saved_cookie_or_session(),
            "comments_foods" : comments_foods,
            "type_foods" : type_foods,
        }    
        return render_template("home/observations_food.html", **data_render)
    elif request.method == "POST":
        text = request.form.get("comment_text")
        id_type_food = request.form.get("type_food")
        commentsFoodController.insert(data={
            "id_admin":managerData.email_to_id_admin(),
            "id_type_food" : id_type_food,
            "comment_text" : text,
        })
        return redirect(url_for("restaurant.observations_food"))


@restaurant.route("/observations_foods_delete", methods=["GET"])
def observations_food_delete():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    row = request.args.get("row")
    commentsFoodController.delete(row)
    return "ok"

@restaurant.route("/observations_foods_get", methods=["GET"])
def observations_food_get():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    row = request.args.get("row")
    comments_foods = commentsFoodController.get_everything({"id_admin":managerData.email_to_id_admin(), "id_type_food":row})
    return comments_foods

# fin observaciones food

# OBERVACIONES DE ORDENES
# @restaurant.route("/reservations")
# def ():

# Reservaciones
@restaurant.route("/reservations")
def reservations():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    id_admin_ = managerData.email_to_id_admin()
    data_query = {"id_admin":id_admin_}
    state_resr = request.args.get("state_reservation")
    key_resr = request.args.get("key_reservation")
    limit_resr = request.args.get("limit")
    if state_resr:
        data_query["only_state"] = state_resr
    if key_resr:
        data_query["reservation_code"] = key_resr
        if ("only_state" in data_query.keys()):
            del(data_query["only_state"])
    if limit_resr:
        data_query["limit"] = limit_resr
    else:
        data_query["limit"] = 10
        
    response_reservations = reservationsFoodsController.get_all(data_query)
    for response in response_reservations:
        total_price_products = 0
        new_data_products = []
        products_reservation = json.loads(response["foods_reservation"].replace("'", '"'))
        id_admin = False
        for product in products_reservation:
            id_food = product["identifier"]
            cantity = int(product["cantity"])
            id_admin = product["app"]  

            food_result = foodModel.show_all_free({"id_food" : id_food, "id_admin" : id_admin})
            if food_result:
                food_result=foodModel.show_all_free({"id_food" : id_food, "id_admin" : id_admin})[0]
                total_price_products = total_price_products + (float(food_result["price"]) * cantity)
                type_food = typeFoodModel.show_all_free({"id_type_food" : food_result["type_food"]})
                if type_food:
                    type_food = typeFoodModel.show_all_free({"id_type_food" : food_result["type_food"]})[0]
                    food_result["type_food"] = type_food["name_type"]
                    food_result["cantity"] = cantity
            new_data_products.append(food_result)
        data_user_app_main = userAppController.read({"id":response["id_user"]})   
        
        response["user_app_name"] = data_user_app_main[0]["last_name"] + ", " + data_user_app_main[0]["first_name"]
        response["user_app_email"] = data_user_app_main[0]["email"]
        response["user_app_number"] = data_user_app_main[0]["tel_whats"]
        response["user_app_profile"] = data_user_app_main[0]["image"]

        response["foods_reservation"] = new_data_products
        response["total_price"] = total_price_products
    dataConfigAdmin = configurationDataController.read({"id_admin":id_admin_})
    data_render = {
        "image_profile" : managerData.image_name_saved_cookie_or_session(),
        "level_user_context" : managerData.level_saved_cookie_or_session(),
        "reservations_data" : response_reservations,
        "data_config_get" : data_query,
        "dataConfigAdmin" : dataConfigAdmin[0],
    }
    return render_template("home/admin/reservations.html", **data_render)

@restaurant.route("/update_state_reservations", methods=["POST"])
def update_state_reservation():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    if request.method == "POST":
        id_reservation = request.form.get("id_reservation")
        state = request.form.get("state")
        if str(state) == "3":
            data_reservation = reservationsFoodsController.get_all({"id":id_reservation})
            if data_reservation:
                resp_box_data = restaurantBoxController.get_all({"id_admin": managerData.email_to_id_admin()})
                id_box = resp_box_data[0]["id"]
                data = data_reservation[0]["foods_reservation"]
                if len(data) > 2:
                    data = data.replace("'", '"')
                    data = json.loads(data)

                amount_all_temp = 0.0
                for f in data:
                    quant = f["cantity"]
                    f_resp = foodModel.show_all_free({"id_food":f["identifier"], "id_admin": managerData.email_to_id_admin()})
                    if f_resp:
                        price = f_resp[0]["price"]
                        total_price = float(quant) * float(price)
                        amount_all_temp += total_price
                
                new_daily_amount_reservation = float(resp_box_data[0]["daily_amount_reservation"]) + amount_all_temp
                restaurantBoxController.update(id_box, {"daily_amount_reservation":new_daily_amount_reservation})

                id_user = 0
                if managerData.level_saved_cookie_or_session() == 4:
                    id_user = managerData.email_to_id()
                new_daily_quantity_reservation = int(resp_box_data[0]["daily_quantity_reservation"]) + 1
                restaurantBoxController.update(id_box, {"daily_quantity_reservation":new_daily_quantity_reservation, "id_user":id_user})
            
        reservationsFoodsController.update_booking({"id_reservation":id_reservation}, {"state_reservation" : state})
        data_reservation = reservationsFoodsController.get_all({"id":id_reservation})
        if data_reservation:
            id_admin = data_reservation[0]["id_admin"]
            id_user = data_reservation[0]["id_user"]
            user_email = userAppController.read({"id":id_user})[0]["email"]
            company_name = usersModel.show_all({"id_admin":id_admin})[0]["company_name"]
            date_reservation = data_reservation[0]["date_reservation"]
            time_reservation = data_reservation[0]["time_reservation"]
            reservation_code = data_reservation[0]["reservation_code"]
            type_reservation = data_reservation[0]["type_reservation"]
            state_reservation = "Error"
            if str(state) == "1": state_reservation = "ACEPTADO"
            elif str(state) == "2": state_reservation = "RECHAZADO"
            elif str(state) == "3": state_reservation = "CONCLUÍDO"

            if type_reservation == 1: type_reservation = "Para mesa"
            elif type_reservation == 2: type_reservation = "Para llevar"
            elif type_reservation == 3: type_reservation = "Delivery"

            message_email = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Notificación de Pedido - Neeva</title></head>
<body style="font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 20px;">
    <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px; background-color: #ffffff; border: 1px solid #ccc; border-radius: 6px; overflow: hidden;">
        <tr><td align="center" style="background-color: #b2e2b2; padding: 10px;"><img src="https://emtorch.pythonanywhere.com/static/images/emTorch-nuevo-256px-256px.transparent.min.png" alt="Neeva" style="display: block; width: 50px; margin-top: 10px;"><h2 style="margin: 0; font-size: 24px; color: #333;">Neeva</h2></td></tr>
        <tr>
            <td style="padding: 20px;">
                <h3 style="color: blue; margin: 0 0 10px;">Nuevo estado</h3>
                <p style="font-size: 16px; color: #333; margin: 0 0 10px;">Su pedido cambió de estado a: <br><strong style="color: #a9c10c; margin-left: 29px;">"{state_reservation}"</strong></p>
                <span style="display: block; font-weight: bold; font-size: 16px; margin-top: 20px;">Detalles del pedido:</span>
                <table border="0" cellpadding="0" cellspacing="0" width="100%" style="margin-top: 10px;">
                    <tr><td style="padding: 5px 0; font-size: 14px; color: #333;"><strong>Llave:</strong></td><td style="padding: 5px 0; font-size: 14px; color: #555;">{reservation_code}</td></tr>
                    <tr><td style="padding: 5px 0; font-size: 14px; color: #333;"><strong>Fecha:</strong></td><td style="padding: 5px 0; font-size: 14px; color: #555;">{date_reservation}</td></tr>
                    <tr><td style="padding: 5px 0; font-size: 14px; color: #333;"><strong>Hora:</strong></td><td style="padding: 5px 0; font-size: 14px; color: #555;">{time_reservation}</td></tr>
                    <tr><td style="padding: 5px 0; font-size: 14px; color: #333;"><strong>Tipo:</strong></td><td style="padding: 5px 0; font-size: 14px; color: #555;">{type_reservation}</td></tr>
                </table>
            </td>
        </tr>
        <tr><td style="padding: 20px; background-color: #272777; color: #d1a9ff;"><h2 style="margin: 0; font-size: 18px;">Remitente:</h2><h4 style="margin: 0; font-size: 16px; color: #e5e1ff;">{company_name}</h4></td></tr>
        <tr><td style="padding: 20px; text-align: center; background-color: #f4f4f4;"><span style="font-size: 12px; color: #6d6de3; line-height: 12px;">Si encuentras algún error o inconveniente, por favor repórtalo en la sección de Soporte dentro de la app. Estamos aquí para ayudarte.</span></td></tr>
    </table>
</body>
</html>
"""

        sendEmail(False, False, user_email, "Nuevo estado", message_email)
    return "ok"

@restaurant.route("/request_data_deletion")
def reuqest_data_deletion():
    return render_template("pages/request_data_deletion.html")

@restaurant.route("/support/page", methods=["GET", "POST"])
def support_page():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    if request.method == "GET":
        data_render = {
            "image_profile" : managerData.image_name_saved_cookie_or_session(),
            "level_user_context" : managerData.level_saved_cookie_or_session(),
        }
        return render_template("home/support_page.html", **data_render)
    else:
        email = request.form.get("email_for_support")
        message = request.form.get("text_for_support")
        files = request.files.getlist("files_for_support")
        state_response_files = uploadFiles.uploadFile(files, PATH_UPLOAD_FILES_SUPPORT)
        response_controller = dataSupportController.create({
            "id_user" : managerData.email_to_id(),
            "level_user" : managerData.level_saved_cookie_or_session(),
            "email": email,
            "message": message,
            "files": json.dumps(state_response_files),
            "state" : 1,
        })

        if response_controller: 
            flash("Se ha enviado correctamente los datos.", "ok")
        else:
            flash("Ocurrió un error al enviar. Vuelva a enviar los datos por favor.", "error")

        return redirect(url_for("restaurant.support_page"))

# configuracion general de caja
@restaurant.route("/box/encrypted/get")
def get_data_box():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    id_admin = managerData.email_to_id_admin()
    response = restaurantBoxController.get_all({"id_admin":id_admin})
    if response:
        return response[0]
    else:
        return False

@restaurant.route("/box/encrypted/upgrade", methods = ["post"])
def update_data_box():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    category = request.form.get("category")
    id_admin = managerData.email_to_id_admin()
    # order = 1, reservation = 2
    data = {"id_admin":id_admin}
    movement_ = ""
    if category == "1":
        data["total_amount_order"] = request.form.get("total_amount")
        data["daily_amount_order"] = request.form.get("daily_amount")
        data["total_quantity_order"] = request.form.get("total_quantity")
        data["daily_quantity_order"] = request.form.get("daily_quantity")
        movement_ = "Se actualizó la caja de órdenes"
    elif category == "2":
        data["total_amount_reservation"] = request.form.get("total_amount")
        data["daily_amount_reservation"] = request.form.get("daily_amount")
        data["total_quantity_reservation"] = request.form.get("total_quantity")
        data["daily_quantity_reservation"] = request.form.get("daily_quantity")
        movement_ = "Se actualizó la caja de reservas"
    else:
        return ""
    
    restaurantBoxController.update(False, data)
    return "ok"

@restaurant.route("/box/encrypted/close")
def close_data_box():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    category = request.args.get("category")
    id_admin = managerData.email_to_id_admin()
    response = restaurantBoxController.get_all({"id_admin":id_admin})
    # order = 1, reservation = 2
    data = {"id_admin":id_admin}
    movement_ = ""
    if category == "1":
        data["total_amount_order"] = response[0]["total_amount_order"] + response[0]["daily_amount_order"]
        data["daily_amount_order"] = 0
        data["total_quantity_order"] = response[0]["total_quantity_order"] + response[0]["daily_quantity_order"]
        data["daily_quantity_order"] = 0
        movement_ = "Caja de órdenes cerrada"
    elif category == "2":
        data["total_amount_reservation"] = response[0]["total_amount_reservation"] + response[0]["daily_amount_reservation"]
        data["daily_amount_reservation"] = 0
        data["total_quantity_reservation"] = response[0]["total_quantity_reservation"] + response[0]["daily_quantity_reservation"]
        data["daily_quantity_reservation"] = 0
        movement_ = "Caja de reservas cerrada"
    else:
        return ""
    res_state = restaurantBoxController.update(False, data)
    
    if res_state:
        return "ok"
    else:
        return ""

@restaurant.route("/mainbox")
def main_box():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    id_admin = managerData.email_to_id_admin()
    
    
    box = mainBoxRestaurantController.read({"id_admin" : id_admin})  
    if box:
        box =  box[0]
    else:
        box = mainBoxRestaurantController.insert({"id_admin" : id_admin,"box_name" : "Caja 1","initial_amount" : 0.0,"current_amount" : 0.0,"opened_by_id" : 0,"closed_by_id" : 0,"opened_by_level" : 0,"closed_by_level" : 0,})

    data_i_e = incomeAndExpenditureBoxController.read({"id_admin" : id_admin, "state" : 1})
    box.data_income = []
    box.data_expenses = []
    box.income = 0
    box.expenses = 0
    box.sum_amount_all = 0 
    box.sum_amt_1, box.sum_amt_2, box.sum_amt_3, box.sum_amt_4, box.sum_amt_5, box.sum_amt_6 = 0, 0, 0, 0, 0, 0

    response_payments = paymentOrderController.read({"id_admin":id_admin, "state":1})
    for d in response_payments:
        if d.amt_1: 
            box.sum_amt_1 += d.amt_1
            box.sum_amount_all += d.amt_1
        if d.amt_2: 
            box.sum_amt_2 += d.amt_2
            box.sum_amount_all += d.amt_2
        if d.amt_3: 
            box.sum_amt_3 += d.amt_3
            box.sum_amount_all += d.amt_3
        if d.amt_4: 
            box.sum_amt_4 += d.amt_4
            box.sum_amount_all += d.amt_4
        if d.amt_5: 
            box.sum_amt_5 += d.amt_5
            box.sum_amount_all += d.amt_5
        if d.amt_6: 
            box.sum_amt_6 += d.amt_6
            box.sum_amount_all += d.amt_6

    for ie in data_i_e:
        if ie.type == 0:
            if ie.amt == 1: 
                box.expenses += ie.amount
            if ie.amt == 2: 
                box.sum_amt_2 -= ie.amount
                box.sum_amount_all -= ie.amount
            if ie.amt == 3: 
                box.sum_amt_3 -= ie.amount
                box.sum_amount_all -= ie.amount
            if ie.amt == 4: 
                box.sum_amt_4 -= ie.amount
                box.sum_amount_all -= ie.amount
            if ie.amt == 5: 
                box.sum_amt_5 -= ie.amount
                box.sum_amount_all -= ie.amount
            if ie.amt == 6: 
                box.sum_amt_6 -= ie.amount
                box.sum_amount_all -= ie.amount
            box.data_expenses.append(ie)
        elif ie.type == 1:
            if ie.amt == 1: 
                box.income += ie.amount
            if ie.amt == 2: 
                box.sum_amt_2 += ie.amount
                box.sum_amount_all += ie.amount
            if ie.amt == 3: 
                box.sum_amt_3 += ie.amount
                box.sum_amount_all += ie.amount
            if ie.amt == 4: 
                box.sum_amt_4 += ie.amount
                box.sum_amount_all += ie.amount
            if ie.amt == 5: 
                box.sum_amt_5 += ie.amount
                box.sum_amount_all += ie.amount
            if ie.amt == 6: 
                box.sum_amt_6 += ie.amount
                box.sum_amount_all += ie.amount
            box.data_income.append(ie)
    
    if box.opened_by_level == 2:
        res = usersModel.show_all({"id_admin":box.opened_by_id})
        box.opened_by_name = res[0]["user_name"]+", "+res[0]["user_surnames"]
    elif box.opened_by_level == 4:
        res = waitressModel.show_all({"id":box.opened_by_id})
        box.opened_by_name = res[0]["first_name"]+", "+res[0]["last_name"]
    if box.closed_by_level == 2:
        res = usersModel.show_all({"id_admin":box.closed_by_id})
        box.closed_by_name = res[0]["user_name"]+", "+res[0]["user_surnames"]
    elif box.closed_by_level == 4:
        res = waitressModel.show_all({"id":box.closed_by_id})
        box.closed_by_name = res[0]["first_name"]+", "+res[0]["last_name"]
        

    data_render = {
        "image_profile" : managerData.image_name_saved_cookie_or_session(),
        "level_user_context" : managerData.level_saved_cookie_or_session(),
        "data_box" : box,
        "data_i_e" : data_i_e, 
    }
    return render_template("home/main_box.html", **data_render)

@restaurant.route("/mainbox/close")
def main_box_close():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    id_admin = managerData.email_to_id_admin()
    user_id = managerData.email_to_id()
    user_level = managerData.level_saved_cookie_or_session()
    mainBoxRestaurantController.update(id_admin, {
        "box_status":0, 
        "closed_by_id" : user_id,
        "closed_by_level" : user_level, 
        "current_amount" : 0,
        "initial_amount" : 0,
        })
    ie_res = incomeAndExpenditureBoxController.read({"id_admin":id_admin, "state":1})
    for ie in ie_res:
        incomeAndExpenditureBoxController.update(ie.id, {"state":0, "id_admin":id_admin})
    payres = paymentOrderController.read({"id_admin":id_admin, "state":1})
    for p in payres:
        paymentOrderController.update(p.id, {"id_admin":id_admin, "state":0})
    
    return {}

@restaurant.route("/mainbox/open", methods = ["POST"])
def main_box_open():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    id_admin = managerData.email_to_id_admin()
    user_id = managerData.email_to_id()
    user_level = managerData.level_saved_cookie_or_session()
    amount = request.form.get("amount")

    mainBoxRestaurantController.update(id_admin, {
        "box_status":1, 
        "closed_by_id" : 0,
        "closed_by_level" : 0, 
        "opened_by_id" : user_id,
        "opened_by_level" : user_level, 
        "current_amount" : amount,
        "initial_amount" : amount,
        })
    
    return {}

@restaurant.route("/mainbox/create", methods = ["POST"])
def main_box_create():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    box_name = request.form.get("box_name")
    id_admin = managerData.email_to_id_admin()
    if box_name:
        box =mainBoxRestaurantController.insert({"id_admin" : id_admin,"box_name" : box_name, "initial_amount" : 0.0,"current_amount" : 0.0,"opened_by_id" : 0,"closed_by_id" : 0,"opened_by_level" : 0,"closed_by_level" : 0,})
    return {}

@restaurant.route("/mainbox/register_ei", methods = ["POST"])
def main_box_register_ei():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    id_admin = managerData.email_to_id_admin()
    type = request.form.get("type")
    motive = request.form.get("motive")
    amount = request.form.get("amount")
    amt = request.form.get("amt")
    resm = mainBoxRestaurantController.read({"id_admin":id_admin})
    if resm:
        resm = resm[0]
        if int(amt) == 1:
            if int(type) == 0:
                mainBoxRestaurantController.update(id_admin, {"current_amount": float(resm.current_amount) - float(amount)})
            elif int(type) == 1:
                mainBoxRestaurantController.update(id_admin, {"current_amount": float(resm.current_amount) + float(amount)})
            else:
                return {}
        
        incomeAndExpenditureBoxController.insert({
            "id_admin" : id_admin,
            "motive" : motive,
            "amount" : amount,
            "amt" : amt,
            "type" : type,
        })

    return {}

@restaurant.route("/mainbox/delete_ei", methods = ["get"])
def main_box_delete_ei():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    id_admin = managerData.email_to_id_admin()
    id = request.args.get("i")
    box = mainBoxRestaurantController.read({"id_admin":id_admin})
    if box:
        box = box[0]
        amount_temp = float(box.current_amount)

        resie = incomeAndExpenditureBoxController.delete({"id":id, "id_admin" : id_admin})
        if resie:
            resie = resie[0]
            if resie.amt == 1:
                if resie.type == 0:
                    amount_temp += float(resie.amount)
                elif resie.type == 1:
                    amount_temp -= float(resie.amount)
                mainBoxRestaurantController.update(id_admin, {"current_amount":amount_temp})

    return {}

@restaurant.route("/table")
def tableShow():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    data_filter = {"id_admin":managerData.email_to_id_admin()}
    category_id = request.args.get("c")
    if category_id:
        data_filter["category_id"] = category_id
    data_table = tableController.read(data_filter)
    table_categories = tableCategoryController.read({"id_admin":managerData.email_to_id_admin()})
    data_render = {
        "image_profile" : managerData.image_name_saved_cookie_or_session(),
        "level_user_context" : managerData.level_saved_cookie_or_session(),
        "data_table":data_table,
        "table_categories" : table_categories,
        "category_selected" : category_id,
    }
    return render_template("home/tables.html", **data_render)

@restaurant.route("/table/details")
def tableDetails():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    id_table = request.args.get("table")
    user_id_search = request.args.get("u")
    level_user_search = request.args.get("l")
    data_user_admin = usersModel.show_all({"id_admin":managerData.email_to_id_admin()})
    data_table = tableController.read({"id_admin":managerData.email_to_id_admin(), "id":id_table})
    data_query_filter = {"id_user_admin":managerData.email_to_id_admin(), "id_table":id_table, "state_order":4}
    order_table = orderModel.get_all_free(data_query_filter)
    number_table = data_table[0].number_table
    state_table = data_table[0].state
    table_status_message = 0
    amount_all_orders = 0
    users_list = []
    user_name_select = "Todos"
    if len(order_table) > 0:

        for order in order_table:
            order.number_table = data_table[0].number_table
            id_user = order.id_user_context
            user_level = order.user_level
            order.total_cost = 0
            if user_level == 2:
                user_data = usersModel.show_all({"id_admin":id_user})
                if user_data: order.user_context_name = user_data[0]["user_name"]+", "+user_data[0]["user_surnames"]
            elif user_level == 4:
                user_data = waitressModel.show_all({"id":id_user})
                if user_data: order.user_context_name = user_data[0].user_first_name+", "+user_data[0].user_last_name
            elif user_level == 5:
                user_data = userAppController.read({"id":id_user})
                if user_data: order.user_context_name = user_data[0]["first_name"]+", "+user_data[0]["last_name"]
            users_list.append({"user_context_name":order.user_context_name, "user_id":id_user, "user_level":user_level})
            for d in order.data_orders:
                food_data = foodModel.show_all_free({"id_food":d.id_food})
                if food_data:
                    d.food_name = food_data[0]["name"]
                    d.price = food_data[0]["price"]
                    d.image_food = food_data[0]["image"]
                    id_category = food_data[0]["type_food"]
                    cat_data = typeFoodModel.show_all_free({"id_type_food":id_category})
                    d.category_name = cat_data[0]["name_type"]
                    order.total_cost = order.total_cost + (float(d.price) * int(d.quantity))
                    
                else:
                    d.food_name = "Error"
                    d.price = 0
                    d.image_food = "Error"
                    d.category_name = "Error"
                    order.total_cost = 0.0

                d.observations = d.observation.split("///")
    else:
        order_table_st = orderModel.get_all_free({"id_user_admin":managerData.email_to_id_admin(), "id_table":id_table, "state_order":[1,21,22,3,]})
        if order_table_st:
            table_status_message = 1 #Aun hay platos en la mesa
        else:
            tableController.update(id_table, {"id_admin":managerData.email_to_id_admin(), "state":1})
            table_status_message = 2 #No hay nada en la mesa

    if user_id_search and level_user_search:
        to_remove = []
        for of in order_table:
            if int(user_id_search) != of.id_user_context or int(level_user_search) != of.user_level:
                to_remove.append(of)
        for item in to_remove:
            order_table.remove(item)
        if order_table:
            user_name_select = order_table[0].user_context_name
    else:
        user_name_select = "Todos"
    for of in order_table:
        for fm in of.data_orders:
                amount_all_orders += (float(fm.price) * int(fm.quantity))
            
    seen, users_list_data = [], []
    for d in users_list:
        if str(d["user_id"]) + str(d["user_level"]) not in seen:
            users_list_data.append(d)
            seen.append(str(d["user_id"]) + str(d["user_level"]))

    data_render = {
        "image_profile" : managerData.image_name_saved_cookie_or_session(),
        "level_user_context" : managerData.level_saved_cookie_or_session(),
        "data_table":data_table[0],
        "order_table":order_table,
        "number_table":number_table,
        "id_table":id_table,
        "state_table":state_table,
        "table_status_message":table_status_message,
        "amount_all_orders" : amount_all_orders,
        "users_list_data":users_list_data,
        "user_name_select":user_name_select,
        "data_user_admin":data_user_admin[0],
        "user_id_search":user_id_search,
        "level_user_search" :level_user_search,
    }
    return render_template("home/tableDetails.html", **data_render)

@restaurant.route("/table/delete")
def tableDelete():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    id = request.args.get("id")
    if id:
        rt = tableController.delete(id)
        if rt:
            list_orders = orderModel.get_all_free({"id_table":id, "state_order":[1,2,3,4], "id_user_admin" : managerData.email_to_id_admin()})
            for l in list_orders:
                dataOrderController.delete({"order_id" : l.id})
            for j in list_orders:
                orderModel.delete({"id":j.id ,"id_user_admin" : managerData.email_to_id_admin()})

    return {}

@restaurant.route("/table/update", methods=["POST"])
def tableUpdate():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    if request.method == "POST":
        data = {"id_admin":managerData.email_to_id_admin()}
        id = request.form.get("id_table_update")
        if request.form.get("number_table_update"):
            data["number_table"] = request.form.get("number_table_update") 
        if request.form.get("limit_number_of_users_update"):
            data["limit_number_of_users"] = request.form.get("limit_number_of_users_update")
        if request.form.get("state_update"):
            data["state"] = request.form.get("state_update")
        if request.form.get("category_id_update"):
            data["category_id"] = request.form.get("category_id_update")

        res = tableController.update(id, data)
    return {}

@restaurant.route("/table/create", methods=["POST"])
def tableCreate():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    if request.method == "POST":
        number_table = request.form.get("number_table")
        limit_number_of_users = request.form.get("limit_number_of_users")
        category_id = request.form.get("category_id")
        state = 1
        id_admin = managerData.email_to_id_admin()
        data_insert = {
            "id_admin":id_admin,
            "number_table":number_table,
            "state":state,
            "limit_number_of_users":limit_number_of_users,
            "category_id":category_id,
        }
        tableController.insert(data_insert)
        
    return {}

@restaurant.route("/table/category/create", methods=["POST"])
def categoryTableCreate():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    if request.method == "POST":
        name = request.form.get("name")
        id_admin = managerData.email_to_id_admin()
        if name:
            data_insert = {
                "id_admin":id_admin,
                "name":name,
            }
            res = tableCategoryController.insert(data_insert)
            # data_json = res.__dict__
            return {}
    
    return {}

@restaurant.route("/table/category/update", methods=["POST"])
def categoryTableUpdate():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    if request.method == "POST":
        name = request.form.get("name")
        id = request.form.get("category_id")
        if name:
            data_update = {
                "name":name,
            }
            res = tableCategoryController.update(id, data_update)
            # data_json = res.__dict__
            return {}
    
    return {}

@restaurant.route("/table/category/delete", methods=["GET"])
def categoryTableDelete():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    id_row = request.args.get("i")
    
    if id_row:
        data_delete = {
            "id":id_row,
            "id_admin" : managerData.email_to_id_admin(),
        }
        res = tableCategoryController.delete(data_delete)
        if res:
            res_table = tableController.read({"category_id":res[0].id, "id_admin":managerData.email_to_id_admin()})
            for t in res_table:
                list_orders = orderModel.get_all_free({"id_table":t.id, "state_order":[1,2,3,4], "id_user_admin" : managerData.email_to_id_admin()})
                for l in list_orders:
                    dataOrderController.delete({"order_id" : l.id})
                for j in list_orders:
                    orderModel.delete({"id":j.id ,"id_user_admin" : managerData.email_to_id_admin()})
            for td in res_table:
                tableController.delete(td.id)
        return {}

    return {}

@restaurant.route("/table/read")
def tableRead():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    id_table = request.args.get("id_table")
    table_data = tableController.read({"id":id_table, "id_admin":managerData.email_to_id_admin()})
    table_data = [data.__dict__ for data in table_data] 
    for d in table_data:
        del(d["_sa_instance_state"])
    return table_data

@restaurant.route("/inventory")
def inventoryShow():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    categories_inventory = inventoryCategoryController.get_all_free({"id_admin":managerData.email_to_id_admin(), "desc":True})
    category_selected = request.args.get("c")
    qm = request.args.get("qm")
    edmax = request.args.get("edmax")
    edmin = request.args.get("edmin")
    data_query_i = {"id_admin":managerData.email_to_id_admin()}
    if category_selected:
        data_query_i["inventory_category_id"] = category_selected
    if qm:
        data_query_i["limit"] = qm
    else:
        data_query_i["limit"] = 100
    if edmax:
        data_query_i["expiration_date_end"] = edmax
    if edmin:
        data_query_i["expiration_date_start"] = edmin
    data_query_i["desc"] = True
    customers = customerInventoryController.get_all_free({"id_admin":managerData.email_to_id_admin(), "limit":100, "desc":True})
    suppliers = supplierInventoryController.get_all_free({"id_admin":managerData.email_to_id_admin(), "limit":100, "desc":True})
    inventories = inventoryController.get_all_free(data_query_i)
    for i in inventories:
        r = supplierInventoryController.get_all_free({"id" : i.id_supplier})
        if r:
            i.supplier_name = r[0].name

    data_render = {
        "image_profile" : managerData.image_name_saved_cookie_or_session(),
        "level_user_context" : managerData.level_saved_cookie_or_session(),
        "categories_inventory" : categories_inventory,
        "inventories" : inventories,
        "category_selected" : category_selected,
        "customers" : customers,
        "suppliers" : suppliers,
    }
    return render_template("home/inventory.html", **data_render)

@restaurant.route("/inventory/get")
def inventoryGet():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    id = request.args.get("i")
    id_admin = managerData.email_to_id_admin()
    r = inventoryController.get_all_free({"id":id, "id_admin":id_admin})
    d_json = {}
    if r and len(r) > 0:
        d_json = r[0].__dict__
        del(d_json["_sa_instance_state"])
    return d_json

@restaurant.route("/inventory/create", methods=["post"])
def inventoryCreate():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    name = request.form.get("name")
    description = request.form.get("description")
    quantity = request.form.get("quantity")
    purchase_price = request.form.get("purchase_price")
    sale_price = request.form.get("sale_price")
    unit_of_measurement = request.form.get("unit_of_measurement")
    expiration_date = request.form.get("expiration_date")
    state = request.form.get("state")
    category_id = request.form.get("category_id")    
    image_id = request.form.get("image_id")
    id_supplier = request.form.get("id_supplier")

    r1 = inventoryController.insert({
        "id_admin":managerData.email_to_id_admin(),
        "category_id":category_id,
        "name":name,
        "description":description,
        "quantity":quantity,
        "purchase_price":purchase_price,
        "sale_price":sale_price,
        "unit_of_measurement":unit_of_measurement,
        "expiration_date":expiration_date,
        "image_id":image_id,
        "state":state,
        "id_supplier" : id_supplier,
    })
    r2 = inventoryController.update(r1.id, {"id_admin":managerData.email_to_id_admin(), "product_code":str(category_id)+managerData.generate_random_letter(3)+str(r1.id)})
    return {}

@restaurant.route("/inventory/update", methods=["post"])
def inventoryUpdate():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    id = request.form.get("id_product")
    name = request.form.get("name")
    description = request.form.get("description")
    quantity = request.form.get("quantity")
    purchase_price = request.form.get("purchase_price")
    sale_price = request.form.get("sale_price")
    unit_of_measurement = request.form.get("unit_of_measurement")
    expiration_date = request.form.get("expiration_date")
    state = request.form.get("state")
    inventory_category_id = request.form.get("inventory_category_id")    
    image_id = request.form.get("image_id")
    id_supplier = request.form.get("id_supplier")

    r1 = inventoryController.update(id, {
        "id_admin":managerData.email_to_id_admin(),
        "inventory_category_id":inventory_category_id,
        "name":name,
        "description":description,
        "quantity":quantity,
        "purchase_price":purchase_price,
        "sale_price":sale_price,
        "unit_of_measurement":unit_of_measurement,
        "expiration_date":expiration_date,
        "image_id":image_id,
        "state":state,
        "id_supplier" : id_supplier,
    })
    return {}

@restaurant.route("/inventory/delete")
def inventoryDelete():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    id = request.args.get("i")
    r1 = inventoryController.delete({"id":id, "id_admin":managerData.email_to_id_admin()})
    return {}

# invetory category
@restaurant.route("/inventory/category/get")
def inventoryCategoryGet():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))

@restaurant.route("/inventory/category/create", methods=["post"])
def inventoryCategoryCreate():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    name = request.form.get("name")
    description = request.form.get("description")
    image = request.files.get("image")
    state = 1
    data = inventoryCategoryController.insert({
        "id_admin" : managerData.email_to_id_admin(),
        "name":name,
        "description":description,
        "state":state,
        "image_id":0,
    })
    return {}

@restaurant.route("/inventory/category/update", methods = ["post"])
def inventoryCategoryUpdate():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    name = request.form.get("name")
    id = request.form.get("category_id")
    data = inventoryCategoryController.update(id, {"name":name, "id_admin":managerData.email_to_id_admin()})
    return {}

@restaurant.route("/inventory/category/delete")
def inventoryCategoryDelete():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    category_id = request.args.get("i")
    r1 = inventoryController.delete({"category_id":category_id, "id_admin":managerData.email_to_id_admin()})
    r2 = inventoryCategoryController.delete({"id":category_id, "id_admin":managerData.email_to_id_admin()})

    return {}

@restaurant.route("/inventory/customer")
def inventoryCustomer():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    customers = customerInventoryController.get_all_free({"id_admin":managerData.email_to_id_admin(), "desc":True})
    data_render = {
        "image_profile" : managerData.image_name_saved_cookie_or_session(),
        "level_user_context" : managerData.level_saved_cookie_or_session(),
        "customers" : customers,
    }
    return render_template("home/inventoryCustomer.html", **data_render)

@restaurant.route("/inventory/customer/read", methods = ["get"])
def inventoryCustomerRead():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    i = request.args.get("i")
    customer = customerInventoryController.get_all_free({"id_admin":managerData.email_to_id_admin(), "id":i})
    customer_dict = {}
    if customer:
        customer_dict = customer[0].__dict__
        del(customer_dict["_sa_instance_state"])
        del(customer_dict["updated_at"])
        del(customer_dict["id_updater"])
        del(customer_dict["id_admin"])
        del(customer_dict["created_at"])
        del(customer_dict["level_updater"])
        del(customer_dict["state"])

    return customer_dict

@restaurant.route("/inventory/customer/create", methods = ["post"])
def inventoryCustomerCreate():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    data = dict(request.form)
    data["id_admin"] = managerData.email_to_id_admin()
    data["state"] = 1
    res = customerInventoryController.insert(data)
    
    return data

@restaurant.route("/inventory/customer/update", methods=["post"])
def inventoryCustomerUpdate():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    
    data = dict(request.form)
    data["id_admin"] = managerData.email_to_id_admin()
    id_customer = data["i"]
    del(data["i"])
    res = customerInventoryController.update(id_customer, data)
    return data

@restaurant.route("/inventory/customer/delete")
def inventoryCustomerDelete():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    i = request.args.get("i")
    if i:
        res = customerInventoryController.delete({"id":i, "id_admin":managerData.email_to_id_admin()})    
    return {}

# ---------------------------------------------
@restaurant.route("/inventory/supplier")
def inventorySupplier():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    suppliers = supplierInventoryController.get_all_free({"id_admin":managerData.email_to_id_admin(), "desc":True})
    data_render = {
        "image_profile" : managerData.image_name_saved_cookie_or_session(),
        "level_user_context" : managerData.level_saved_cookie_or_session(),
        "suppliers" : suppliers,
    }
    return render_template("home/inventorySupplier.html", **data_render)

@restaurant.route("/inventory/supplier/read", methods = ["get"])
def inventorySupplierRead():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    i = request.args.get("i")
    supplier = supplierInventoryController.get_all_free({"id_admin":managerData.email_to_id_admin(), "id":i})
    supplier_dict = {}
    if supplier:
        supplier_dict = supplier[0].__dict__
        del(supplier_dict["_sa_instance_state"])
        del(supplier_dict["updated_at"])
        del(supplier_dict["id_updater"])
        del(supplier_dict["id_admin"])
        del(supplier_dict["created_at"])
        del(supplier_dict["level_updater"])
        del(supplier_dict["state"])

    return supplier_dict

@restaurant.route("/inventory/supplier/create", methods = ["post"])
def inventorySupplierCreate():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    data = dict(request.form)
    data["id_admin"] = managerData.email_to_id_admin()
    data["state"] = 1
    res = supplierInventoryController.insert(data)
    
    return data

@restaurant.route("/inventory/supplier/update", methods=["post"])
def inventorySupplierUpdate():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    
    data = dict(request.form)
    data["id_admin"] = managerData.email_to_id_admin()
    id_supplier = data["i"]
    del(data["i"])
    res = supplierInventoryController.update(id_supplier, data)
    return data

@restaurant.route("/inventory/supplier/delete")
def inventorySupplierDelete():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    i = request.args.get("i")
    if i:
        res = supplierInventoryController.delete({"id":i, "id_admin":managerData.email_to_id_admin()})    
    return {}
# -----------------------------
@restaurant.route("/inventory/sales", methods=["get"])
def inventorySales():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    data_filter = {"id_admin":managerData.email_to_id_admin(), "desc":True, "product_code":""}
    if request.args.get("product_code"):
        data_filter["product_code"] = request.args.get("product_code")
    if request.args.get("product"):
        data_filter["id_product"] = request.args.get("product")
    if request.args.get("customer"):
        data_filter["customer"] = request.args.get("customer")
    if request.args.get("state"):
        data_filter["state"] = request.args.get("state")
    if request.args.get("date_start"):
        data_filter["date_start"] = request.args.get("date_start")
    if request.args.get("date_end"):
        data_filter["date_end"] = request.args.get("date_end")
    
    sales_list_remove = []
    customers = customerInventoryController.get_all_free({"id_admin":managerData.email_to_id_admin(), "desc":True})
    products = inventoryController.get_all_free({"id_admin":managerData.email_to_id_admin(), "desc":True})
    data_user_admin = usersModel.show_all({"id_admin":managerData.email_to_id_admin()})
    sales_data = salesInventoryController.get_all_free(data_filter)
    for sale in sales_data:
        resi = inventoryController.get_all_free({"id":sale.id_product})
        if resi:
            if data_filter["product_code"] and resi[0].product_code != data_filter["product_code"]:
                sales_list_remove.append(sale)
                continue
            sale.product_name = resi[0].name
            sale.product_code = resi[0].product_code
            sale.product_sale_price = resi[0].sale_price
            sale.product_unit_of_measurement = resi[0].unit_of_measurement
            sale.total_cost = resi[0].sale_price * sale.quantity
            sale.total_cost = sale.total_cost - (sale.total_cost * (sale.discount/100))
        if str(sale.customer).isnumeric():
            res1 = customerInventoryController.get_all_free({"id":sale.customer})
            if res1:
                sale.customer_name = res1[0].name
                sale.customer_company_name = res1[0].company_name
        else:
            sale.customer_name = sale.customer
    if data_filter["product_code"]:
        sales_data = [sale for sale in sales_data if sale not in sales_list_remove]
    
    data_render = {
        "image_profile" : managerData.image_name_saved_cookie_or_session(),
        "level_user_context" : managerData.level_saved_cookie_or_session(),
        "data_user_admin" : data_user_admin[0],
        "sales_data" : sales_data,
        "products" : products,
        "customers" : customers,
    }
    return render_template("home/inventorySales.html", **data_render)

@restaurant.route("/inventory/sales/create", methods=["post"])
def inventorySalesCreate():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    
    data = dict(request.form)
    
    data["id_admin"] = managerData.email_to_id_admin()
    if int(data["customer"]) == 0:
        data["customer"] = data["customer_other"]
        del(data["customer_other"])
    else:
        del(data["customer_other"])
    data["discount"] = data["discount"] if data["discount"] else 0.0
    data["amount_unsettled"] = data["amount_unsettled"] if data["amount_unsettled"] else 0.0
    data["amount_due"] = data["amount_due"] if data["amount_due"] else 0.0
    if data["state"] == "1":
        data["amount_due"] = 0
        data["amount_unsettled"] = 0
    elif data["state"] == "2":
        data["amount_due"] = 0
    elif data["state"] == "3":
        data["amount_unsettled"] = 0

    res1 = inventoryController.get_all_free({"id":data["id_product"], "id_admin":managerData.email_to_id_admin()})
    if res1:
        quantity_product = res1[0].quantity
        new_quantity = float(quantity_product) - float(data["quantity"])
        inventoryController.update(data["id_product"],{"id_admin":managerData.email_to_id_admin(), "quantity":new_quantity}) 
        salesInventoryController.insert(data)
        return data
    else:
        return {}

@restaurant.route("/inventory/sales/update", methods=["post"])
def inventorySalesUpdate():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    
    data = dict(request.form)
    data["id_admin"] = managerData.email_to_id_admin()
    res = salesInventoryController.get_all_free({"id":data["id"], "id_admin":managerData.email_to_id_admin()})
    if res:
        res = res[0]
        inv = inventoryController.get_all_free({"id":res.id_product, "id_admin":managerData.email_to_id_admin()})
        if inv:
            price = inv[0].sale_price
        
            discount = 0
            if res.discount:
                discount = res.discount
            total_cost = round((res.quantity * price) - (discount/100 * (res.quantity * price)), 2)
            data_update_sale = {"id_admin": managerData.email_to_id_admin()}
            if res.state == 2:
                print(round(float(data["amount_update"]), 2),  res.amount_unsettled)
                if round(float(data["amount_update"]), 2) > res.amount_unsettled:
                    flash("El monto a cobrar debe ser menor o igual a: "+ str(res.amount_unsettled), "warning")
                    return {}
            elif res.state == 3:
                if round(float(data["amount_update"]), 2) > res.amount_due:
                    flash("El monto a abonar debe ser menor o igual a: "+ str(res.amount_due), "warning")
                    return {}

            if round(float(data["amount_update"]) + res.amount_paid, 2) == total_cost:
                data_update_sale["amount_unsettled"] = 0
                data_update_sale["amount_due"] = 0
                data_update_sale["amount_paid"] = total_cost
                data_update_sale["state"] = 1
            elif round(float(data["amount_update"]) + res.amount_paid, 2) < total_cost:
                data_update_sale["amount_unsettled"] = round(res.amount_unsettled - float(data["amount_update"]), 2)
                data_update_sale["amount_paid"] = round(float(data["amount_update"]) + res.amount_paid, 2)
                data_update_sale["state"] = 2
                if data_update_sale["amount_unsettled"] == 0:
                    data_update_sale["amount_unsettled"] = 0
                    data_update_sale["state"] = 1
            elif round(float(data["amount_update"]) + res.amount_paid, 2) > total_cost:
                data_update_sale["amount_unsettled"] = 0
                if float(data["amount_update"]) <= res.amount_due:
                    data_update_sale["amount_due"] = round(total_cost - round(res.amount_paid - float(data["amount_update"]), 2), 2) * -1
                    data_update_sale["amount_paid"] = round(res.amount_paid - float(data["amount_update"]), 2)
                    data_update_sale["state"] = 3
                    if data_update_sale["amount_due"] == 0:
                        data_update_sale["amount_due"] = 0
                        data_update_sale["state"] = 1
                else:
                    flash("* El monto a abonar debe ser menor o igual a: "+ str(res.amount_due), "warning")
                    return {}

            salesInventoryController.update(data["id"], data_update_sale)

            
    return data

@restaurant.route("/inventory/sales/delete", methods=["get"])
def inventorySalesDelete():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    
    id = request.args.get("i")
    id_admin = managerData.email_to_id_admin()
    res = salesInventoryController.delete({"id":id, "id_admin":id_admin})
    return {}

# ---------------------------------------
@restaurant.route("/inventory/report", methods=["get"])
def inventoryReport():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    data_user_admin = usersModel.show_all({"id_admin":managerData.email_to_id_admin()})
    data_filter = {"id_admin":managerData.email_to_id_admin(), "desc":True, "product_code":""}
    if request.args.get("product_code"):
        data_filter["product_code"] = request.args.get("product_code")
    if request.args.get("product"):
        data_filter["id_product"] = request.args.get("product")
    if request.args.get("customer"):
        data_filter["customer"] = request.args.get("customer")
    if request.args.get("state"):
        data_filter["state"] = request.args.get("state")
    if request.args.get("date_start"):
        data_filter["date_start"] = request.args.get("date_start")
    if request.args.get("date_end"):
        data_filter["date_end"] = request.args.get("date_end")
    
    sales_list_remove = []
    customers = customerInventoryController.get_all_free({"id_admin":managerData.email_to_id_admin(), "desc":True})
    products = inventoryController.get_all_free({"id_admin":managerData.email_to_id_admin(), "desc":True})
    sales_data = salesInventoryController.get_all_free(data_filter)
    data_report_result = {
        "quantity_sold" : 0,
        "amount_paid" : 0,
        "amount_unsettled" : 0,
        "amount_due" : 0,
        "total_amount_at_sale_price" : 0,
        "total_amount_at_purchase_price" : 0,
        "total_discount" : 0,
        "overall_profi_no_discountt" : 0,
        "overall_profi_with_discountt" : 0,

        "best_selling_product" : "",
        "least_sold_product" : "",
        "frequent customer" : "",
    }
    for sale in sales_data:
        resi = inventoryController.get_all_free({"id":sale.id_product})
        data_report_result["quantity_sold"] += sale.quantity
        data_report_result["amount_paid"] += sale.amount_paid 
        data_report_result["amount_unsettled"] += sale.amount_unsettled
        data_report_result["amount_due"] += sale.amount_due
        if resi:
            if data_filter["product_code"] and resi[0].product_code != data_filter["product_code"]:
                sales_list_remove.append(sale)
                continue
            sale.product_name = resi[0].name
            sale.product_code = resi[0].product_code
            sale.product_sale_price = resi[0].sale_price
            sale.product_unit_of_measurement = resi[0].unit_of_measurement
            sale.total_cost = resi[0].sale_price * sale.quantity
            data_report_result["total_amount_at_sale_price"] += sale.total_cost
            sale.total_cost = sale.total_cost - (sale.total_cost * (sale.discount/100))
            data_report_result["total_discount"] += round(sale.total_cost * (sale.discount/100), 2)
            data_report_result["total_amount_at_purchase_price"] += resi[0].purchase_price * sale.quantity 
        if str(sale.customer).isnumeric():
            res1 = customerInventoryController.get_all_free({"id":sale.customer})
            if res1:
                sale.customer_name = res1[0].name
                sale.customer_company_name = res1[0].company_name
        else:
            sale.customer_name = sale.customer
    data_report_result["overall_profit_no_discount"] = round(data_report_result["total_amount_at_sale_price"] - data_report_result["total_amount_at_purchase_price"], 2)
    data_report_result["overall_profit_with_discount"] = round(data_report_result["total_amount_at_sale_price"] - data_report_result["total_amount_at_purchase_price"] - data_report_result["total_discount"], 2)
    if data_filter["product_code"]:
        sales_data = [sale for sale in sales_data if sale not in sales_list_remove]
    
    data_render = {
        "image_profile" : managerData.image_name_saved_cookie_or_session(),
        "level_user_context" : managerData.level_saved_cookie_or_session(),
        "data_user_admin" : data_user_admin,
        "sales_data" : sales_data,
        "data_report_result" : data_report_result,
        "customers" : customers,
        "products" : products,
        "data_filter" : data_filter,
    }
    return render_template("home/inventoryReport.html", **data_render)

@restaurant.route("/schedule", methods=["get"])
def schedule():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))

    data_render = {
        "image_profile" : managerData.image_name_saved_cookie_or_session(),
        "level_user_context" : managerData.level_saved_cookie_or_session(),
    }
    return render_template("home/schedule.html", **data_render)

@restaurant.route("/schedule/read", methods=["get"])
def schedule_read():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    id_admin = managerData.email_to_id_admin()
    date_time_now = datetime.datetime.now()
    data = availabilityCalendarController.read({"id_admin":id_admin , "date_start":date_time_now})
    data_json = []
    for d in data:
        data_json.append(d.__dict__)
    
    list_del = ["_sa_instance_state", "created_at", "updated_at", "id_admin"]
    for d in data_json:
        if "T" in d["end"]:
            d["allDay"] = False
        for k in list(d.keys()): 
            if not d[k] or k in list_del:
                del(d[k])

    return data_json

@restaurant.route("/schedule/create", methods=["post"])
def schedule_create():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    id_admin = managerData.email_to_id_admin()
    data_json = request.get_json()
    data_json["id_admin"] = id_admin
    if data_json["start"]:
        availabilityCalendarController.insert(data_json)
    return data_json

@restaurant.route("/schedule/update", methods=["post"])
def schedule_update():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    id_admin = managerData.email_to_id_admin()
    data_json = request.get_json()
    data_json["id_admin"] = id_admin
    id_ = data_json["id"]
    del(data_json["id"])
    if data_json["start"]:
        availabilityCalendarController.update(id_ , data_json)
    return data_json

@restaurant.route("/schedule/delete", methods=["get"])
def schedule_delete():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    id_admin = managerData.email_to_id_admin()
    id = request.args.get("id")
    res = availabilityCalendarController.delete({"id" : id, "id_admin" : id_admin})
    return {}

@restaurant.route("/images", methods=["get"])
def images():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    id_admin = managerData.email_to_id_admin()
    food_icons = imageFoodController.show_all({"id_admin":id_admin})
    data_render = {
        "image_profile" : managerData.image_name_saved_cookie_or_session(),
        "level_user_context" : managerData.level_saved_cookie_or_session(),
        "food_icons" : food_icons,
    }
    return render_template("home/images.html", **data_render)

@restaurant.route("/images/create", methods=["post"])
def images_create():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    id_admin = managerData.email_to_id_admin()
    food_name = request.form.get("food_name")
    food_image = uploadFiles.uploadFile(request.files.get("food_image"), PATH_UPLOAD_ICONS_FOOD)

    imageFoodController.insert({
        "id_admin": id_admin,
        "name":food_name,
        "url_name" : food_image,
    })
    return redirect(url_for("restaurant.images"))

@restaurant.route("/images/update", methods=["post"])
def images_update():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    id_admin = managerData.email_to_id_admin()
    image_id = request.form.get("image_id")
    food_name = request.form.get("food_name_update")
    food_image = uploadFiles.uploadFile(request.files.get("food_image_update"), PATH_UPLOAD_ICONS_FOOD)
    data = {}
    if food_name:
        data["name"] = food_name
    if food_image:
        data["url_name"] = food_image
    imageFoodController.update(image_id , data)
    flash("Se ha actualizado los datos.", "ok")
    return redirect(url_for("restaurant.images"))

@restaurant.route("/images/delete", methods=["get"])
def images_delete():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    id_admin = managerData.email_to_id_admin()
    id_image = request.args.get("image_id_delete")
    imageFoodController.delete(id_image)
    flash("Se ha eliminado correctamente la imagen.", "ok")
    return redirect(url_for("restaurant.images"))

@restaurant.route("/images/get", methods=["get"])
def images_get():
    if not managerData.logged_user(): return redirect(url_for("pages.loginApp"))
    id_admin = managerData.email_to_id_admin()
    search = request.args.get("search")
    id_image = request.args.get("id_image")
    if search:
        if len(search)>0:
            icons = imageFoodController.show_all({
                "word_to_search" : search,
                "id_admin" : id_admin,
                "limit" : 4,
            })
            return icons
        else:
            return []
    elif id_image:
        if len(id_image)>0:
            icons = imageFoodController.show_all({
                "id" : id_image,
                "id_admin" : id_admin,
            })
            return icons
        else:
            return []
    else:
        return []
    










# CLOSE APP
@restaurant.route("/closeprogram")
def destroySession():
    user_email = request.cookies.get("user_email")
    if user_email:
        response = make_response(redirect(url_for("pages.loginApp")))
        response.delete_cookie('user_email')
        return response
    
    elif "user_email" in session:
        session.clear()
    
    return redirect(url_for("pages.loginApp"))
    
    