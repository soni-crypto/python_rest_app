import json
from datetime import datetime
from flask import Blueprint, render_template, request, redirect
from ..controllers.restaurant.foodDishes import Food
from ..controllers.restaurant.typeFoodABS import TypeFood_ABS
from ..controllers.restaurant.userController import UsersAdmin
from application.controllers.restaurant.waitressController import WaitressMainC
from ..controllers.restaurant.reservationsFoodsController import ReservationsFoodsController
from application.controllers.restaurant.usersAppController import UsersAppController

from application.helpers.upload_files import UploadFiles
from application.helpers.mail_admin import sendEmail

foodController = Food()
typeFoodController = TypeFood_ABS()
userController = UsersAdmin()
reservationsFoodsController = ReservationsFoodsController()
userAppController = UsersAppController()
waitressController = WaitressMainC()
uploadFiles = UploadFiles()

PATH_UPLOAD_IMAGES_VOUCHERS = "application/views/static/images/userapp/vouchers_reservations/"

pages_admin = Blueprint("pages_admin", __name__)

@pages_admin.route("/")
def home():
    data_render = {
        ""
    }
    return render_template("pages_admin/pages_main.html")

@pages_admin.route("/s/<url_id>")
def page_by_id(url_id):
    data = userController.show_all({"id_secondary":url_id})
    type_food_data = []
    if len(data) > 0:
        id_admin = data[0]["id"]
        type_food_data = typeFoodController.show_all({"id_admin":id_admin})
        for type_food in type_food_data:
            food_data = foodController.show_all_free({"id_type_food":type_food["id"]})
            type_food["foods_all"] = food_data
    else:
        print("sin datos")
    
    data_render = {
        "data_admin" : data[0],
        "type_food_data" : type_food_data,
    }
    return render_template("pages_admin/pages_main.html" , **data_render)

@pages_admin.route("/pay")
def page_pay_product_view():
    return render_template("pages_admin/page_pay.html" )

@pages_admin.route("/pay/main", methods=["GET","POST"])
def page_pay_product_pay():

    return {}
@pages_admin.route("/pay/save_reservation", methods=["GET","POST"])
def page_pay_save_reservation():
    id_user = request.cookies.get("id")
    if request.method == "POST":
        date_reservation = request.form.get("date_reservation")
        if date_reservation:
            date_reservation = datetime.strptime(date_reservation, "%Y-%m-%d").date()
        time_reservation = request.form.get("time_reservation")
        if time_reservation:
            time_reservation = datetime.strptime(time_reservation, "%H:%M").time()
        type_reservation = request.form.get("type_reservation")
        message_reservation = request.form.get("message_reservation")
        voucher_reservation = uploadFiles.uploadFile(request.files.get("voucher_reservation"), PATH_UPLOAD_IMAGES_VOUCHERS)
        if not voucher_reservation: voucher_reservation = ""
        products_reservation = request.form.get("products")
        my_location_coordinate = request.form.get("my_location_coordinate")
        price_per_delivery = request.form.get("price_per_delivery")
        products_reservation = json.loads(products_reservation)
        id_admin = products_reservation[0]["app"]
        for product in products_reservation:
            del(product["price_unique"])
        
        # Aqui para guardar datos y ver reservas
        # print(date_reservation, time_reservation, type_reservation, message_reservation, products_reservation)

        id_reservation = reservationsFoodsController.create_booking(data={
            "reservation_code": "null",
            "id_admin" : id_admin,
            "id_user" : id_user,
            "date_reservation" : date_reservation,
            "time_reservation" : time_reservation,
            "type_reservation" : type_reservation,
            "message_reservation" : str(message_reservation),
            "foods_reservation" : str(products_reservation),
            "vouchers_reservations" : str(voucher_reservation),
            "conversation_reservation" : "",
            "user_coordinates" : my_location_coordinate,
            "price_per_delivery" : price_per_delivery,
        })
        reservation_code = str(id_admin)+"-"+str(id_user)+str(id_reservation)
        reservationsFoodsController.update_booking({"id_reservation":id_reservation}, {"reservation_code": reservation_code})
        data_user = userAppController.read({"id":id_user})[0]
        user_app_name_all = data_user["first_name"] + ", " + data_user["last_name"]
        email_admin = UsersAdmin.show_all({"id_admin": id_admin})[0]
        email_admin = email_admin["user_email"]
        if int(type_reservation) == 1:
            type_reservation_text = "Para mesa"
        elif int(type_reservation) == 2:
            type_reservation_text = "Para llevar"
        elif int(type_reservation) == 3:
            type_reservation_text = "Delivery"
        else:
            type_reservation_text = "Error"
        message_for_admin = """
                        <!DOCTYPE html>
                        <html lang="es">
                        <head>
                            <meta charset="UTF-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">
                            <style>
                            body {font-family: Arial, sans-serif;background-color: #f4f4f4;margin: 0;padding: 20px;}
                            .email-container {max-width: 600px;background-color: #ffffff;margin: 0 auto;border-radius: 8px;box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);overflow: hidden;}
                            .header {background-color: #4CAF50;color: white;padding: 20px;text-align: center;}
                            .header h1 {margin: 0;font-size: 24px;}
                            .content {padding: 20px;border: 1px solid #dfd4d4;}
                            .content h2 {margin-top: 0;}
                            .reservation-details {border-top: 1px solid #e0e0e0;margin-top: 20px;padding-top: 20px; }
                            .reservation-details table {width: 100%;border-collapse: collapse;}
                            .reservation-details th, .reservation-details td {text-align: left;padding: 8px;border-bottom: 1px solid #e0e0e0;}
                            .reservation-details th {background-color: #f8f8f8;}
                            .footer {background-color: #4CAF50;color: white;text-align: center;padding: 10px;font-size: 14px;}
                            </style>
                        </head>"""+ f"""
                        <body>
                            <div class="email-container">
                                <div class="header"><h1>¡Nueva Reserva!</h1></div>
                                <div class="content">
                                    <h2>Pendiente:</h2>
                                    <p>Por favor, revise los detalles a continuación:</p>
                                    <div class="reservation-details">
                                        <h3>Detalles de la Reserva</h3>
                                        <table>
                                            <tr><th>Cliente</th><td>{user_app_name_all}</td></tr>
                                            <tr><th>Código</th><td>{reservation_code}</td></tr>
                                            <tr><th>Fecha de Reserva</th><td>{date_reservation}</td></tr>
                                            <tr><th>Hora</th><td>{time_reservation}</td></tr>
                                            <tr><th>Tipo de reserva</th><td>{type_reservation_text}</td></tr>
                                        </table>
                                    </div>
                                    <p>Por favor, revisa y confirma la validez de esta reserva en la sección de Reservas de Neeva ADM.</p>
                                </div>
                                <div class="footer"><p>&copy; 2023 - 2024 Neeva ADM. Todos los derechos reservados.</p></div>
                            </div>
                        </body>
                        </html>"""
                        
        sendEmail(False, False, email_admin, "Nueva reserva", message_for_admin)
        users_all = waitressController.show_all({"partner_id" : id_admin})
        for i in users_all:
            sendEmail(False, False, i["user_email"], "Nueva reserva", message_for_admin)
        return "ok"
    else:
        return "error"

@pages_admin.route("/pay/prepared", methods=["GET"])
def data_prepared_product():
    id_food = request.args.get("identifier")
    cantity_food = request.args.get("cantity")
    id_admin = request.args.get("app")
    
    food_all = foodController.show_all_free({"id_food":id_food, "id_admin":id_admin})
    if food_all:
        try:
            food = food_all[0]
            total_price = float(food["price"]) * int(cantity_food)
            food["total_price"] = "{:.2f}".format(total_price)
            type_food = typeFoodController.show_all_free({"id_type_food":food["type_food"]})[0]["name_type"]
            food["type_food"] = type_food
            food["cantity"] = cantity_food
            return food
        
        except Exception as error:
            print("Error: ", error)
            return {}
    else:
        return {}
    
@pages_admin.route("/pay/data/admin", methods=["GET"])
def data_prepared_admin():
    id_admin = request.args.get("app")
    data_admin = userController.show_id(id_admin)
    if data_admin:
        return data_admin
    else:
        return {}