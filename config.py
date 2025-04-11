
class Config:
    TEMPLATE_FOLDER = "views/templates"
    STATIC_FOLDER = "views/static"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@localhost/proyecto_python" 
    
    # correo para pruebas
    EMAIL_MESSAGE_USER = "neeva.message@gmail.com"
    EMAIL_MESSAGE_PASSWORD = "aenh yglo sojv bfqf"

    CLOUDINARY = False # poner en True solo si completas los datos de abajo
    CLOUDINARY_CLOUD_NAME = ""
    CLOUDINARY_API_KEY = ""
    CLOUDINARY_API_SECRET = ""