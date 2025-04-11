from flask_sqlalchemy import SQLAlchemy

from flask import current_app
db = SQLAlchemy()
"""
tipos de usuario
2 administradores o dueños de un negocio
4 usuarios que pertenecen a aun administrador, es diferente al rol de usuario
5 usuarios de la applicacion de android
6 usuarios libres que vienen de la pagina del administrador al hacer una orden
7 usuarios registrados cuando hacen pago en caja
""" 

class PaymentOrder(db.Model):
    __tablename__ = 'payment_order'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    id_admin = db.Column(db.Integer, nullable = False)
    
    amt_1 = db.Column(db.Numeric(10, 2), nullable = True) # efectivo
    amt_2 = db.Column(db.Numeric(10, 2), nullable = True) # tarjeta
    amt_3 = db.Column(db.Numeric(10, 2), nullable = True) # yape
    amt_4 = db.Column(db.Numeric(10, 2), nullable = True) # plin
    amt_5 = db.Column(db.Numeric(10, 2), nullable = True) # paypal
    amt_6 = db.Column(db.Numeric(10, 2), nullable = True) # Otros
    
    state = db.Column(db.Integer, nullable = False, default = 1) # 1-> proceso, 2-> cerrado(concluído)
    order_or_table_id = db.Column(db.Integer, nullable=False)
    mode = db.Column(db.Integer, nullable = False) #1-> por oden , 2-> por mesa
    box_id = db.Column(db.Integer, nullable = True, default = None)

    def __repr__(self) -> str:
        return f'<Model: {self.id}>'
    
class OrderDishes(db.Model):
    __tablename__ = 'order_dishes'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    order_code = db.Column(db.String(50), default=None)
    state_order = db.Column(db.Integer) # 1-> orden creado, 21->orden en cocina(aceptado), 22->orden en cocina(en proceso), 3-> orden preparada, 4-> orden en mesa, 5-> orden concluido, 6->orden rechazado
    id_user_admin = db.Column(db.Integer, nullable = False)
    id_user_context = db.Column(db.Integer)
    user_level = db.Column(db.Integer, nullable=True)
    id_table = db.Column(db.Integer)

    data_orders = db.relationship("DataOrder", backref = "data", lazy=True)
    
    def __repr__(self):
        return f'<Model: {self.id}>'

class DataOrder(db.Model):
    __tablename__ = 'data_order'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    id_admin = db.Column(db.Integer, nullable = True)
    id_food = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    type_order = db.Column(db.Integer) # 1-> mesa, 2-> llevar
    observation = db.Column(db.String(255), nullable=True, default=None)
    order_dishes_id = db.Column(db.Integer, db.ForeignKey("order_dishes.id"), nullable=False)
    
    def __repr__(self):
        return f'<Model: {self.id}>'

class Table(db.Model):
    __tablename__ = 'table'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    id_admin = db.Column(db.Integer)
    id_user_app = db.Column(db.Integer, nullable = True, default = None)
    table_closer_id = db.Column(db.Integer, nullable = True, default = None) # id cerrador de mesa
    table_closer_level = db.Column(db.Integer, nullable = True, default = None) # level cerrador de mesa
    limit_number_of_users = db.Column(db.Integer, nullable = True, default = None)
    number_table = db.Column(db.Integer)
    state = db.Column(db.Integer, default = 1) # 1-> libre, 2->ocupado, 3->reservado
    category_id = db.Column(db.Integer, nullable = True, default = None)

    def __repr__(self):
        return f'<Model: {self.id}>'

class FoodDishes (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    name = db.Column(db.String(100))
    preparation_time = db.Column(db.Integer, nullable = True,  default = 0) 
    description = db.Column(db.String(200))
    type_food = db.Column(db.Integer)
    price = db.Column(db.Float)
    product_code = db.Column(db.String(50), nullable = True, default = "")
    image = db.Column(db.String(200))
    state = db.Column(db.Integer)
    id_user_admin = db.Column(db.Integer)
        
    def __repr__(self):
        return f"<Model: {self.name}>"

class TypeFoodABS(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    name_type = db.Column(db.String(100))
    description = db.Column(db.String(250), default="")
    image = db.Column(db.String(200))
    state = db.Column(db.Integer)
    id_user_admin = db.Column(db.Integer)
    
    def __repr__(self):
        return f"<Model: {self.name_type}>"
    

class AmountMainCollect(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    created_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    amount_main = db.Column(db.Float)
    amount_diary = db.Column(db.Float)
    id_user_admin = db.Column(db.Integer)
    
    def __repr__(self):
        return f"<Model: Amount>"

# Cuando un admin te envia una solictud de trabajo
class JobApplication(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    created_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    id_user = db.Column(db.Integer)
    id_admin = db.Column(db.Integer)
    job_status = db.Column(db.Integer, default=1)
    
    def __repr__(self):
        return f"<Model: JobApplicaction>"
    
# NOTIFICACIONES PARA TODOS 
class Notifications(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    created_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    id_sender = db.Column(db.Integer)
    level_sender = db.Column(db.Integer, default=0)
    id_receiver = db.Column(db.Integer)
    level_receiver = db.Column(db.Integer, default=0)
    title = db.Column(db.String(100), default="")
    text = db.Column(db.String(350), default="")
    link = db.Column(db.String(300), default="")
    status = db.Column(db.Integer, default=1)
    
    def __repr__(self):
        return f"<Model: Notifications>"
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)    
    id_secondary = db.Column(db.String(100), default="")
    
    created_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    subscription_start_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    subscription_end_date = db.Column(db.DateTime, default= None)

    user_name = db.Column(db.String(50))
    user_surnames = db.Column(db.String(50))
    user_email = db.Column(db.String(50))
    user_number = db.Column(db.String(22))
    user_password = db.Column(db.String(15))
    user_image = db.Column(db.String(200), default="")
    user_type = db.Column(db.Integer, default=2)
    user_key_room_app = db.Column(db.String(50))

    
    company_location_1 = db.Column(db.String(250), default="")
    company_location_2 = db.Column(db.String(250), default="")
    company_location_3 = db.Column(db.String(250), default="")
    company_location_4 = db.Column(db.String(250), default="")
    company_location_coord = db.Column(db.String(250), default="")
    company_description = db.Column(db.Text, default="")
    company_name = db.Column(db.String(100), default="")
    company_image = db.Column(db.String(200), default="")
    company_icon = db.Column(db.String(200), default="")

    cash_payment_status = db.Column(db.Integer, default=0)
    
    yape_payment_status = db.Column(db.Integer, default=0)
    izipayya_payment_status = db.Column(db.Integer, default=0)
    bizum_payment_status = db.Column(db.Integer, default=0)

    yape_payment_image = db.Column(db.String(200), default="")
    izipayya_payment_image = db.Column(db.String(200), default="")
    bizum_payment_image = db.Column(db.String(200), default="")
    
    qr_code_image = db.Column(db.String(200), default = None, nullable = True)

    # id_country = db.Column(db.Integer)

    def __repr__(self):
        return f"<Model: User>"
    
    
class StockHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    id_user_captured = db.Column(db.Integer)
    order_code = db.Column(db.String(50), nullable = True, default="")
    added_amount = db.Column(db.String(150))
    movement_created = db.Column(db.String(150))
    description_action = db.Column(db.String(255))
    id_user_admin = db.Column(db.Integer)
    user_level = db.Column(db.Integer, nullable = True)
    
    def __repr__(self):
        return f"<Model: StockHistory>"
    
class WaitressData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_secondary = db.Column(db.String(100), default="")
    created_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    user_role = db.Column(db.Integer) # 1-> mesero, 2-> cocinero, 3-> driver
    user_first_name = db.Column(db.String(50))
    user_last_name = db.Column(db.String(50))
    user_phone_number = db.Column(db.String(20))
    user_email = db.Column(db.String(55))
    user_password = db.Column(db.String(120))
    user_image = db.Column(db.String(200))
    partner_id = db.Column(db.Integer)
    user_type = db.Column(db.Integer, default=4)
    p_create_1 = db.Column(db.Integer, default = 0)
    p_update_1 = db.Column(db.Integer, default = 0)
    p_delete_1 = db.Column(db.Integer, default = 0)
    p_confirm_1 = db.Column(db.Integer, default = 0)
    box_id = db.Column(db.Integer, nullable = True, default = None)
    
    def __repr__(self):
        return f"<Model: {self.user_first_name}>"

class FreeUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    id_admin = db.Column(db.Integer)
    user_level = db.Column(db.Integer)

    name = db.Column(db.String(100), default = "")
    phone_number = db.Column(db.String(20), default = "")
    email = db.Column(db.String(55), default = "")
    address = db.Column(db.String(255), default = "")
    
    def __repr__(self):
        return f"<Model: {self.name}>"

class Jobs(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    created_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    id_admin = db.Column(db.Integer)
    job_title = db.Column(db.String(255))
    job_details = db.Column(db.String(255))
    job_location = db.Column(db.String(350))
    job_minimum_salary = db.Column(db.Integer, default = 0)
    job_maximum_salary = db.Column(db.Integer, default = 0)
    job_salary_time = db.Column(db.String(55)) #Modalidad de pago mensual, semanal, quincenal, etc    
    job_type = db.Column(db.Integer, default = 0) # Medio tiempo, Tiempo completo, sabados y domingo
    job_status = db.Column(db.Integer, default=1)
    
    def __repr__(self):
        return f"<Model: Jobs>"
    
class AvailableCountries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    country_name = db.Column(db.String(100))
    country_image = db.Column(db.String(200))
    country_code = db.Column(db.String(5))
    country_state = db.Column(db.Integer, default=1)
    
    def __repr__(self):
        return f"<Model: AvailableCountries>"

class CommentsFood(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    order_num = db.Column(db.Integer, default=0)
    id_admin = db.Column(db.Integer)
    id_type_food = db.Column(db.Integer, default=0)
    comment_text =db.Column(db.String(300))
    
    def __repr__(self):
        return f"<Model: CommentsFood>"
    
class ReservationsFoods(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    reservation_code = db.Column(db.String(25), nullable=True, default = None)
    id_admin = db.Column(db.Integer)
    id_user = db.Column(db.Integer)
    date_reservation = db.Column(db.Date)
    time_reservation = db.Column(db.Time)
    type_reservation = db.Column(db.Integer)
    message_reservation = db.Column(db.String(255))
    foods_reservation = db.Column(db.Text) # contiene un una lista de json que trae dentro id de cada comida
    vouchers_reservations = db.Column(db.Text)

    conversation_reservation = db.Column(db.Text) # lista de comversacion
    state_reservation = db.Column(db.Integer, default=0) # estado de la reserva => 0:en proceso, 1:aceptado, 2:rechazado, 3:concluido
    user_coordinates = db.Column(db.String(255), default=None, nullable=True)
    price_per_delivery = db.Column(db.Float, default = 0.0 , nullable = False)
    
    def __repr__(self):
        return f"<Model: ReservationsFoods>"

class UserApp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    first_name = db.Column(db.String(60))
    last_name = db.Column((db.String(60)))
    email = db.Column(db.String(60))
    tel_whats = db.Column(db.String(15))
    password = db.Column(db.String(40))
    image = db.Column(db.String(200), default=None, nullable=True)
    location = db.Column(db.Text, default=None, nullable=True)
    favorite_foods = db.Column(db.String(255), default=None, nullable=True) # lista
    favorite_admins = db.Column(db.String(255), default=None, nullable=True) #lista
    stars = db.Column(db.Text(), default=None, nullable=True) #lista
    
    def __repr__(self):
        return f'<Model: {self.first_name}>'

class ServicePaymentRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    id_user = db.Column(db.Integer, nullable = False)
    message = db.Column(db.Text, default=None,  nullable=True)
    image_voucher = db.Column(db.String(200))
    state = db.Column(db.Integer, default=1)
    
    def __repr__(self):
        return f'<Model: {self.id}>'
    
class ImageFood(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    id_admin = db.Column(db.Integer, nullable = False)
    name = db.Column(db.String(80), nullable = False)
    url_name = db.Column(db.String(255), nullable = False)
    state = db.Column(db.Integer, default=1)
    
    def __repr__(self):
        return f'<Model: {self.id}>'

class DataSupport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    id_user = db.Column(db.Integer, nullable = False)
    level_user = db.Column(db.Integer, nullable = False)
    email = db.Column(db.String(255), nullable = True)
    message = db.Column(db.Text, nullable = True)
    files = db.Column(db.Text, nullable = True)
    state = db.Column(db.Integer, default=1) # 1  en proceso, 2 concluído
    
    def __repr__(self):
        return f'<Model: {self.id}>'

class RestaurantBox(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    id_admin = db.Column(db.Integer, nullable = False)
    id_user = db.Column(db.Integer, nullable = False)

    total_amount_order = db.Column(db.Float, nullable = False, default = 0)
    daily_amount_order = db.Column(db.Float, nullable = False, default = 0)
    total_quantity_order = db.Column(db.Integer, nullable = False, default = 0)
    daily_quantity_order = db.Column(db.Integer, nullable = False, default = 0)

    total_amount_reservation = db.Column(db.Float, nullable = False, default = 0)
    daily_amount_reservation = db.Column(db.Float, nullable = False, default = 0)
    total_quantity_reservation = db.Column(db.Integer, nullable = False, default = 0)
    daily_quantity_reservation = db.Column(db.Integer, nullable = False, default = 0)

    state = db.Column(db.Integer, default=1)
    
    def __repr__(self):
        return f'<Model: {self.id}>'
    
class MainBoxRestaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    id_admin = db.Column(db.Integer, nullable = False)
    
    box_name = db.Column(db.String(255), nullable = True, default="")
    initial_amount = db.Column(db.Numeric(10, 2), nullable = False, default = 0)
    current_amount = db.Column(db.Numeric(10, 2), nullable = False, default = 0)
    opened_by_id = db.Column(db.Integer, nullable = True, default = 0)
    closed_by_id = db.Column(db.Integer, nullable = True, default = 0)
    opened_by_level = db.Column(db.Integer, nullable = True, default = 0)
    closed_by_level = db.Column(db.Integer, nullable = True, default = 0)

    box_status = db.Column(db.Integer, default = 0) #0 -> cerrado , 1-> abierto
    
    def __repr__(self):
        return f'<Model: {self.id}>'

class IncomeAndExpenditureBox(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    id_admin = db.Column(db.Integer, nullable = False)
    
    amt = db.Column(db.Integer, nullable = True, default = 1)
    box_id = db.Column(db.Integer, nullable = True, default = None)
    motive = db.Column(db.String(300), nullable = True, default="")
    amount = db.Column(db.Numeric(10, 2), nullable = False, default = 0)
    type = db.Column(db.Integer, nullable = False) # 0->Egreso, 1->Ingreso 
    state = db.Column(db.Integer, default = 0) #0 -> cerrado , 1-> abierto
    
    def __repr__(self):
        return f'<Model: {self.id}>'


class ConfigurationData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    id_admin = db.Column(db.Integer, nullable = False) 
    
    email = db.Column(db.String(80), nullable = True, default="")
    password_email = db.Column(db.String(50), nullable = True, default="")
    language = db.Column(db.String(80), nullable = True, default="")
    currency = db.Column(db.String(15), nullable = True, default="")
    time_zone = db.Column(db.String(50), nullable = True, default="America/Lima")
    order_now = db.Column(db.Integer, nullable = True, default=0) # 0 -> no, 1->si 
    order_now = db.Column(db.Integer, nullable = True, default=0) # 0 -> no, 1->si 
    delivery_accept = db.Column(db.Integer, nullable = True, default=0) # 0 -> no, 1->si
    reservations_accept = db.Column(db.Integer, nullable = True, default=0) # 0 -> no, 1->si
    visibility_in_app = db.Column(db.Integer, nullable = True, default=0) # 0 -> no, 1->si
    send_email_1 = db.Column(db.Integer, nullable = True, default=0) # 0 -> no, 1->si ##enviar correo por cambio de estado de reservas
    send_email_2 = db.Column(db.Integer, nullable = True, default=0) # 0 -> no, 1->si ##enviar voucher por correo
    maximum_distance_range = db.Column(db.Float, nullable = False, default = 70)
    price_per_delivery = db.Column(db.Float, nullable = True, default=0.0)
    
    def __repr__(self):
        return f'<Model: {self.id}>'

class TableCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    id_admin = db.Column(db.Integer, nullable = False)
    name = db.Column(db.String(80), nullable = True, default="Default")
    state = db.Column(db.Integer, nullable = True, default=1)

    def __repr__(self):
        return f'<Model: {self.name}>'


class InventoryCategory (db.Model):
    __tablename__ = "inventory_category"
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    id_admin = db.Column(db.Integer, nullable = False)
    name = db.Column(db.String(50), nullable = True, default="")
    description = db.Column(db.Text, nullable = True, default = "")
    image_id = db.Column(db.Integer, nullable = False, default = 0)
    state = db.Column(db.Integer, nullable = True, default=1)
    data_inventories = db.relationship("Inventory", backref = "category", lazy = True)

    def __repr__(self):
        return f'<Model: {self.name}>'
    
class Inventory(db.Model):
    __tablename__ = "inventory" 
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    id_admin = db.Column(db.Integer, nullable = False)
    id_updater = db.Column(db.Integer, nullable = True, default = None)
    level_updater = db.Column(db.Integer, nullable = True, default = None)
    inventory_category_id = db.Column(db.Integer, db.ForeignKey("inventory_category.id"), nullable=False)
    id_supplier = db.Column(db.Integer, nullable = True)
    product_code = db.Column(db.String(50), nullable = True, default="")
    name = db.Column(db.String(90), nullable = True, default="")
    description = db.Column(db.Text, nullable = True, default = "")
    quantity = db.Column(db.Integer, nullable = False, default = 0)
    purchase_price = db.Column(db.Float, nullable=False, default = 0.0)
    sale_price = db.Column(db.Float, nullable=False, default = 0.0)
    unit_of_measurement = db.Column(db.String(10), nullable = True, default="")
    expiration_date = db.Column(db.String(15), nullable=True, default = "")
    image_id = db.Column(db.Integer, nullable = False, default = 0)
    state = db.Column(db.Integer, nullable = True, default=1)

    def __repr__(self):
        return f'<Model: {self.name}>'

class CustomerInventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    id_admin = db.Column(db.Integer, nullable = False)
    id_updater = db.Column(db.Integer, nullable = True, default = None)
    level_updater = db.Column(db.Integer, nullable = True, default = None)
    
    name = db.Column(db.String(80), nullable = True, default="")
    company_name = db.Column(db.String(80), nullable = True, default="")
    description = db.Column(db.String(255), nullable = True, default="")
    address = db.Column(db.String(100), nullable = True, default="")
    city = db.Column(db.String(50), nullable = True, default="")
    country = db.Column(db.String(50), nullable = True, default="")
    email = db.Column(db.String(50), nullable = True, default="")
    phone = db.Column(db.String(20), nullable = True, default="")
    tax_id = db.Column(db.String(20), nullable = True, default="") # ruc, cuit, rut, nit, cif, ein, rfc
    bank_account_number = db.Column(db.String(34), nullable = True, default="")
    state = db.Column(db.Integer, nullable = True, default=1)

    def __repr__(self):
        return f'<Model: {self.name}>'
    
class SupplierInventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    id_admin = db.Column(db.Integer, nullable = False)
    id_updater = db.Column(db.Integer, nullable = True, default = None)
    level_updater = db.Column(db.Integer, nullable = True, default = None)
    
    name = db.Column(db.String(80), nullable = True, default="")
    company_name = db.Column(db.String(80), nullable = True, default="")
    description = db.Column(db.String(255), nullable = True, default="")
    address = db.Column(db.String(100), nullable = True, default="")
    city = db.Column(db.String(50), nullable = True, default="")
    country = db.Column(db.String(50), nullable = True, default="")
    email = db.Column(db.String(50), nullable = True, default="")
    phone = db.Column(db.String(20), nullable = True, default="")
    tax_id = db.Column(db.String(20), nullable = True, default="") # ruc, cuit, rut, nit, cif, ein, rfc
    bank_account_number = db.Column(db.String(34), nullable = True, default="")
    state = db.Column(db.Integer, nullable = True, default=1)

    def __repr__(self):
        return f'<Model: {self.name}>'
    

class SalesInventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    id_admin = db.Column(db.Integer, nullable = False)
    id_updater = db.Column(db.Integer, nullable = True, default = None)
    level_updater = db.Column(db.Integer, nullable = True, default = None)

    id_product = db.Column(db.Integer) # id del producto del inventario
    customer = db.Column(db.String(80), nullable = True, default = None)
    quantity = db.Column(db.Float)
    discount = db.Column(db.Float, nullable = False, default = 0.0)
    pay_method = db.Column(db.Integer, nullable = True) #1-> efectivo, 2-> targeta, 3-> yape, 4-> otros
    amount_unsettled = db.Column(db.Float, nullable = False, default = 0.0)
    amount_due = db.Column(db.Float, nullable = False, default = 0.0)
    amount_paid = db.Column(db.Float, nullable = False, default = 0.0)
    state = db.Column(db.Integer, nullable = True, default=1) # 1-> completado, 2-> por cobrar, 3->por abonar, 

    def __repr__(self):
        return f'<Model: {self.id}>'

class AvailabilityCalendar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    id_admin = db.Column(db.Integer, nullable = False)

    title = db.Column(db.String(255))
    start = db.Column(db.String(50), nullable = True, default = None)
    end = db.Column(db.String(50), nullable = True, default = None)
    color = db.Column(db.String(50), nullable = True, default = None)
    backgroundColor = db.Column(db.String(50), nullable = True, default = None)
    textColor = db.Column(db.String(50), nullable = True, default = None)
    borderColor = db.Column(db.String(50), nullable = True, default = None)
    display = db.Column(db.String(50), nullable = True, default = None)
    overlap = db.Column(db.String(50), nullable = True, default = None)
    groupId = db.Column(db.String(50), nullable = True, default = None)
    constraint = db.Column(db.String(150), nullable = True, default = None)

    state = db.Column(db.Integer, nullable = True, default=1)
    def __repr__(self):
        return f'<Model: {self.title}>'
    
class RequestFromPage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    id_admin = db.Column(db.Integer, nullable = False)
    id_user = db.Column(db.Integer, nullable = False, default = 0)
    requested_date = db.Column(db.String(30), nullable = False)
    requested_time = db.Column(db.String(30), nullable = False)
    type = db.Column(db.Integer, nullable = True, default=1) # 1->reserva, 2->delivery
    state = db.Column(db.Integer, nullable = True, default=1) # 1->comenzando, 2->solicitado, 3-> aceptado, 4->concluido, 5->rechazado.

class RequestFromPageData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    id_admin = db.Column(db.Integer, nullable = False)
    id_user = db.Column(db.Integer, nullable = False, default = 0)
    id_request_from_page = db.Column(db.Integer, nullable = False)
    id_food =  db.Column(db.Integer, nullable = False)
    quantity =  db.Column(db.Integer, nullable = False, default = 1)
    type =  db.Column(db.Integer, nullable = False, default = 1)
    state = db.Column(db.Integer, nullable = True, default=1) # 1->solicitado, 2-> aceptado, 3->concluido, 4->rechazado.

def createDB(app):
    with app.app_context():
        db.create_all()