from app import db, app
from flask import redirect, render_template, url_for, abort, Blueprint
from flask_login import  current_user, login_required
from ..models import Project, Flight, Log
from werkzeug.utils import secure_filename
from datetime import datetime
import os
##### LOG MANAGEMENT ROUTES AND VIEWS
log = Blueprint('log', __name__)

#   SUPPOSEDLY LOG UPLOAD ROUTE BUT DOESN'T WORK
@log.route('/upload', methods=['POST'])
@login_required
def upload_log(f,flight):
    filename = secure_filename(user.username + f.filename)
        
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    return redirect(url_for('flight.view_flight', flight_id=flight.flight_id))



@log.route('/log/delete/<log_id>', methods=['GET','DELETE'])
@login_required
def delete_log(log_id):
    log = Log.query.get(log_id)
    if log is None:
        abort(404)

    flight_id = log.flight_id
    flight = Flight.query.get(flight_id)
    project = Project.query.get(flight.project_id)
    
    
    if current_user.id != project.user_id:
        abort(404)
    else:
        os.remove(os.path.join(app.config['ORIGINAL_LOG_FILE_FOLDER'], log.filename))

        if log.gps_filename is not None:
            os.remove(os.path.join(app.config['GPS_COORDINATE_FILE_FOLDER'], log.gps_filename))
        
        os.remove(os.path.join(app.config['PROCESSED_OUTPUT_FILE_FOLDER'], log.processed_filename))
        db.session.delete(log)
        db.session.commit()
        
        return redirect(url_for('flight.view_flight', flight_id=flight_id))

