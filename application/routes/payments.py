from flask import Blueprint, render_template, request, redirect, url_for, session, flash, get_flashed_messages
import paypalrestsdk
from application.helpers.upload_files import UploadFiles

from application.helpers.gestor_restaurant import ManagerData
from application.controllers.restaurant.JobsController import JobsController
from application.controllers.restaurant.controllerServicePaymentRequest import ControllerServicePaymentRequest
from ..controllers.restaurant.userController import UsersAdmin

payments = Blueprint("payments", __name__)

managerData = ManagerData()
userController = UsersAdmin()
jobsController = JobsController()
controllerServicePaymentRequest = ControllerServicePaymentRequest()
uploadFiles = UploadFiles()

PATH_UPLOAD_IMAGE_VOUCHER = "application/views/static/images/images_restaurant/onlyadmin/vouchers_admin/"


paypalrestsdk.configure({
    "mode": "live", # sandbox or live
    "client_id": "PONER AQUI EL CLIENT ID DE PAYPAL",
    "client_secret": "PONER AQUI EL CLIENT SECRET DE PAYPAL" 
    })

@payments.route("/app_payments")
def home():
    data_spr = controllerServicePaymentRequest.read({})
    data_render = {
                "image_profile" : managerData.image_name_saved_cookie_or_session(),
                "level_user_context" : managerData.level_saved_cookie_or_session(),
            }
    return render_template("/home/payments.html", **data_render)

@payments.route("/payment_send_save", methods=["post"])
def paymentSave():
    if request.method == "POST":
        id_user = managerData.email_to_id_admin()
        message = request.form.get("message")
        voucher = request.files.get("voucher")
        voucher_image = uploadFiles.uploadFile(voucher, PATH_UPLOAD_IMAGE_VOUCHER)
        if voucher_image:
            controllerServicePaymentRequest.create({
                "id_user": id_user,
                "message" : message,
                "image_voucher" : voucher_image,
                "state" : 1,
            })
            flash("Los datos se han enviado correcatmente.", "ok")
            flash("Dentro de un momento validaremos su pago.", "warning")
            return "ok"
        return "error"
    return "error"

@payments.route("/pay_with_paypal", methods=["GET", "POST"])
def pay_paypal():
    
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": "http://192.168.0.103:5000/payments/processing",
            "cancel_url": "http://192.168.0.103:5000/payments/cancel"
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "item",
                    "sku": "item",
                    "price": "1.00",
                    "currency": "USD",
                    "quantity": 1
                }]
            },
            "amount": {
                "total": "1.00",
                "currency": "USD"
            },
            "description": "This is the payment transaction description."
        }]
    })

    if payment.create():
        return redirect(payment.links[1].href)
    else:
        return 'Error creating payment:' + payment.error["message"]

@payments.route("/processing")    
def processing():
    payment = paypalrestsdk.Payment.find(request.args.get('paymentId'))

    if payment.execute({'payer_id': request.args.get('PayerID')}):
        print("PROCESSING payment")
    else:
        print('Error executing payment:', payment.error)
    return ("Pago exitoso")

@payments.route('/cancel', methods=["POST","GET"])
def paymentCancel():
    return 'Payment canceled!'