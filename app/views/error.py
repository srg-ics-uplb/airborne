from flask import Blueprint, render_template
from flask_login import current_user
#####   ERROR HANDLERS

error = Blueprint('error', __name__)

@error.app_errorhandler(403)
def error_403(e):
    return render_template("error_403.html", title="403 Forbidden")


@error.app_errorhandler(404)
def error_404(e):
    return render_template("error_404.html", title="404 Not Found")

@error.app_errorhandler(401)
def error_401(e):
    return render_template("error_401.html", title="401 Unauthorized")


