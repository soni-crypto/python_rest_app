from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(404)
def not_found_error(error):
    return render_template('pages/404.html'), 404

@errors.app_errorhandler(500)
def internal_error(error):
    return render_template('pages/500.html'), 500

@errors.app_errorhandler(503)
def service_unavailable_error(error):
    return render_template('pages/503.html'), 503

@errors.app_errorhandler(Exception)
def handle_exception(e):
    return render_template("pages/error_general.html", error=e), 500

@errors.app_errorhandler(502)
def bad_gateway_error(error):
    return render_template('pages/502.html'), 502