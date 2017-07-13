from app import app, db #still needs app for config
from flask import render_template, redirect, url_for, request, abort, Blueprint
from ..forms import FlightForm, LogForm
from ..models import Project, Drone, Flight, Log
from flask_login import  current_user, login_required
from werkzeug.utils import secure_filename
from datetime import datetime
import os, subprocess, json

#####   FLIGHT MANAGEMENT ROUTES AND VIEWS
flight = Blueprint('flight', __name__)

#   VIEW ALL FLIGHTS
@flight.route('/flights')
@login_required
def view_all_flights():
    user = current_user
    
    #get projects of user
    project_ids = db.session.query(Project.id).filter_by(user_id = user.id)

    #get flights from projects
    flights = Flight.query.filter(Flight.project_id.in_(project_ids)).all()

    #get projects for flights
    for flight in flights:
        flight.project = Project.query.get(flight.project_id)

    #get drones used in flights
    for flight in flights:
        flight.drone = Drone.query.get(flight.drone_id)

    flight_count=len(flights)
    return render_template("flights.html", title="Flights", user=user, flights=flights, flight_count = flight_count)

#VIEW FLIGHT DETAILS
@flight.route('/flight/view/<flight_id>', methods=['GET','POST'])
@login_required
def view_flight(flight_id):
    user = current_user
    flight = Flight.query.get(flight_id)
    
    if flight is None:
        abort(404)
    
    project = Project.query.get(flight.project_id)
    
    if current_user.id != project.user_id:
        abort(404)
    

    drone = Drone.query.get(flight.drone_id)
    logs = Log.query.filter_by(flight_id=flight_id).all()
    for log in logs:
         log.processed_content = json.loads(log.content)
         log.processed_content['timestamp'] = datetime.fromtimestamp(log.processed_content['timestamp']/1000000)

         print "Log " + log.filename + " successfully processed"    
    

    form = LogForm()

    if form.validate_on_submit():
        f = form.log_file.data
        h = form.log_file.data
        filename = secure_filename(user.username + ' - ' + str(datetime.now()) +' - '+ f.filename )
        
        # attempt to get gps coordinates when uploaded file is a text dump (*.log)
        gps_name = filename.rsplit('.', 1) 
        print h
        if gps_name[1] == "log":
            print 'yay itlog'
            g = open(app.config['GPS_COORDINATE_FILES_FOLDER']+'\\'+gps_name[0]+'.map', 'w')
            for line in h:
                a = line.split(',', 1)
                if a[0] == "GPS":
                    g.write(a[1])

            g.close()
            
        f.seek(0)
        # save file
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        #open dronekit-la and capture output
        print app.config['LOG_ANALYZER_DIR'] + app.config['UPLOAD_FOLDER'] + '\\' + filename
        args = app.config['LOG_ANALYZER_DIR'] + app.config['UPLOAD_FOLDER'] + '\\' + filename
        content = subprocess.check_output(args)
        
        #save contents to db to avoid running dronekit-la again
        log = Log(filename, content, flight_id)
        
        db.session.add(log)
        db.session.commit()
        print 'Upload Successful for file: ' + filename
        redirect(url_for('flight.view_flight', flight_id=flight_id))

    return render_template('view_flight.html', title=flight.name,  flight=flight, drone=drone, project=project, form=form, logs=logs)

#   ADD A FLIGHT
@flight.route('/flight/add', methods=['GET','POST'])
@login_required
def add_flight():
    user = current_user
    projects = db.session.query(Project.id, Project.name).filter_by(user_id = user.id)
    drones = db.session.query(Drone.id, Drone.name).filter_by(user_id = user.id)
    form= FlightForm()
    form.project.choices= projects
    form.drone.choices = drones

    if form.validate_on_submit():
        duration = (form.duration_hours.data*60*60)+(form.duration_mins.data*60)+(form.duration_secs.data)
        flight = Flight(
            form.name.data,
            form.location.data,
            form.date.data,
            duration,
            form.flight_type.data,
            form.more_type_info.data,
            form.operation_type.data,
            form.night_flight.data,
            form.landing_count.data,
            form.travelled_distance.data,
            form.max_agl_altitude.data,
            form.notes.data,
            form.weather_description.data,
            form.drone.data,
            form.project.data
        )

        print flight

        db.session.add(flight)
        db.session.commit()
        return redirect(url_for("flight.view_all_flights"))

    return render_template("flight_form.html", title="Add Flight", form_title="Add Flight", submit_value="Add Flight", name="add_flight", projects=projects, form=form)

#   EDIT FLIGHT DETAILS
@flight.route('/flight/edit/<flight_id>', methods=['GET','POST'])
@login_required
def edit_flight(flight_id):
    user = current_user
    flight = Flight.query.get(flight_id)
    if flight is None:
        abort(404)

    project = Project.query.get(flight.project_id)
    
    if current_user.id != project.user_id:
        abort(404)
    
    else:
        projects = db.session.query(Project.id, Project.name).filter_by(user_id = user.id)
        drones = db.session.query(Drone.id, Drone.name).filter_by(user_id = user.id)
        form= FlightForm(obj=flight)
        form.duration_hours.data = flight.duration/ 3600
        form.duration_mins.data = (flight.duration % 3600) / 60
        form.duration_secs.data = flight.duration % 60
        form.project.choices= projects
        form.drone.choices = drones
        
        if form.validate_on_submit():
            duration = (form.duration_hours.data*60*60)+(form.duration_mins.data*60)+(form.duration_secs.data)
            flight.name = form.name.data
            flight.location = form.location.data
            flight.date = form.date.data
            flight.duration = duration
            flight.more_type_info = form.more_type_info.data
            flight.operation_type = form.operation_type.data
            flight.night_flight = form.night_flight.data
            flight.landing_count = form.landing_count.data
            flight.travelled_distance = form.travelled_distance.data
            flight.max_agl_altitude = form.max_agl_altitude.data
            flight.notes = form.notes.data
            flight.weather_description = form.weather_description.data
            flight.drone_id = form.drone.data
            flight.project_id =  form.project.data
            
            print flight

            db.session.commit()
            return redirect(url_for("flight.view_all_flights"))
        return render_template("flight_form.html", title="Edit Flight", form_title="Edit Flight Details", submit_value="Save Changes", name="edit_flight", projects=projects, form=form)

#   DELETE A FLIGHT
@flight.route('/flight/delete/<flight_id>')
@login_required
def delete_flight(flight_id):
    flight = Flight.query.get(flight_id)
    if flight is None:
        abort(404)
    
    project = Project.query.get(flight.project_id)
    
    if current_user.id != project.user_id:
        abort(404)
    
    else:
        db.session.delete(flight)
        db.session.commit()
        return redirect(url_for("flight.view_all_flights"))
