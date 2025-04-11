from datetime import datetime
from application.controllers.restaurant.availableCountries import availableCountries
from application.controllers.restaurant.userController import UsersAdmin
from application.controllers.restaurant.imageFoodController import ImageFoodController
from flask import Blueprint, render_template, redirect, url_for, request

from application.helpers.upload_files import UploadFiles
from application.controllers.restaurant.controllerServicePaymentRequest import ControllerServicePaymentRequest
from ..controllers.restaurant.reservationsFoodsController import ReservationsFoodsController

admin_emtorch = Blueprint("admin_emtorch", __name__)

userAdminController = UsersAdmin()
availableCountriesController = availableCountries()
uploadfilesController = UploadFiles()
controllerServicePaymentRequest = ControllerServicePaymentRequest()
imageFoodController = ImageFoodController()
reservationsFoodsController = ReservationsFoodsController()

PATH_UPLOAD_ICONS_COUNTRY = "application/views/static/images/images_restaurant/onlyadmin/countries/"
PATH_UPLOAD_ICONS_FOOD = "application/views/static/images/images_restaurant/onlyadmin/icon_food/"

@admin_emtorch.route("/")
def index():
    return render_template("onlyadmin/index.html")

@admin_emtorch.route("/home")
def home():
    return render_template("onlyadmin/home.html")

@admin_emtorch.route("/country")
def country():
    countries = availableCountriesController.get_everything()
    print(countries)
    return render_template("onlyadmin/country.html")

@admin_emtorch.route("/country/create", methods=["POST"])
def country_create():
    if request.method == "POST":
        country_name = request.form.get("country_name")
        country_image = uploadfilesController.uploadFile(request.files.get("country_image"), PATH_UPLOAD_ICONS_COUNTRY)
        country_code = request.form.get("country_code")
        country_state = 1
        res = availableCountriesController.insert(data={
            "country_name": country_name,
            "country_image": country_image,
            "country_code": country_code,
            "country_state": country_state,
        })
    return redirect(url_for("admin_emtorch.country"))

@admin_emtorch.route("/country/update")
def country_update():
    return redirect(url_for("admin_emtorch.country"))

@admin_emtorch.route("/country/delete")
def country_delete():
    return redirect(url_for("admin_emtorch.country"))

@admin_emtorch.route("/payments/control")
def payments_control():
    data = controllerServicePaymentRequest.read()
    if data:
        for i in data:
            user_data = userAdminController.show_all({
                "id_admin" : i["id_user"],
            })
            if user_data:
                i["user_number"] = user_data[0]["user_number"]
                i["user_email"] = user_data[0]["user_email"]
                i["user_name"] = user_data[0]["user_name"]
                i["user_surnames"] = user_data[0]["user_surnames"]

                i["subscription_start_date"] = user_data[0]["subscription_start_date"]
                i["subscription_end_date"] = user_data[0]["subscription_end_date"]

            print(i)
    data_render = {
        "data_payments" : data,
    }
    
    return render_template("onlyadmin/payments_control.html", **data_render)

# images food controll
@admin_emtorch.route("/images/imagesfood")
def images_food():
    food_icons = imageFoodController.show_all({})
    return render_template("/onlyadmin/imagesfoods.html", food_icons=food_icons)

@admin_emtorch.route("/images/imagesfood/save", methods=["POST"])
def images_food_save():
    if request.method == "POST":
        food_name = request.form.get("food_name")
        food_image = uploadfilesController.uploadFile(request.files.get("food_image"), PATH_UPLOAD_ICONS_FOOD)
        imageFoodController.insert({
            "name":food_name,
            "url_name" : food_image,
        })
    return redirect(url_for("admin_emtorch.images_food"))

@admin_emtorch.route("/images/imagesfood/delete/<id>", methods=["GET"])
def images_food_delete(id):
    if str(id).isdigit():
        image_data = imageFoodController.show_all({"id":int(id)})
        if image_data and len(image_data) > 0:
            url_name = image_data[0]["url_name"]
            uploadfilesController.deleteFile(PATH_UPLOAD_ICONS_FOOD, url_name)
            imageFoodController.delete(id)
    return redirect(url_for("admin_emtorch.images_food"))

@admin_emtorch.route("/api/v1/icon/food/search")
def api_food():
    search = request.args.get("search")
    if len(search)>0:
        icons = imageFoodController.show_all({
            "word_to_search" : search,
        })
        return icons
    else:
        return []

@admin_emtorch.route("/emtorch/policy_and_privacy")
def policy_and_privacy():
    return render_template("policy_and_privacy.html")

@admin_emtorch.route("/data/reservation/delete", methods=["GET", "POST"])
def delete_reservation():
    if request.method == "GET":
        return render_template("onlyadmin/control_data_reservation.html")
    else: 
        max_date = request.form.get("max_date")
        password = request.form.get("password")
        reservationsFoodsController.delete_booking({"max_date":max_date, "password":password})
        return redirect(url_for("admin_emtorch.delete_reservation"))
    

