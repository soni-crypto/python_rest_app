from config import Config
from flask import Flask, session, render_template
from flask_migrate import Migrate
from application.routes.restaurantApp import restaurant
from application.routes.jobsApp import jobs
from application.routes.payments import payments
from application.routes.pages_admin import pages_admin
from application.routes.user_app import user_app
from application.routes.admin_emtorch import admin_emtorch
from application.routes.pages import pages
from application.routes.errors import errors
from application.routes.page_client import page_client

app = Flask(__name__, static_folder=Config.STATIC_FOLDER, template_folder=Config.TEMPLATE_FOLDER) #instance_path
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SQLALCHEMY_DATABASE_URI"] = Config.SQLALCHEMY_DATABASE_URI

app.config["SECRET_KEY"] = "ludovico1234567890"


from .models import Restaurant

Restaurant.db.init_app(app)
Restaurant.createDB(app) # ejecutar solo una vez
migrate = Migrate(app, Restaurant.db)

app.register_blueprint(pages, url_prefix="/")
app.register_blueprint(restaurant, url_prefix="/honey")
app.register_blueprint(jobs, url_prefix="/honey/jobs")
app.register_blueprint(payments, url_prefix = "/payments")
app.register_blueprint(pages_admin, url_prefix="/pages")
app.register_blueprint(user_app, url_prefix="/userapp")
app.register_blueprint(admin_emtorch, url_prefix="/onlyadmin")
app.register_blueprint(page_client, url_prefix="/p")
def register_error_handlers(app):
    # Manejo de errores
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('pages/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('pages/500.html'), 500

    @app.errorhandler(503)
    def service_unavailable_error(error):
        return render_template('pages/503.html'), 503

    @app.errorhandler(502)
    def bad_gateway_error(error):
        return render_template('pages/502.html'), 502
    
register_error_handlers(app)