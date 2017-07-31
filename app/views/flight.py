"""
        View module for Flights. This module defines routes and logic for Flight-related things.
"""
import os
import json
import platform
from datetime import datetime
from app import app, db #still needs app for config
from flask import render_template, redirect, url_for, abort, Blueprint
from app.views.log import create_map, write_log_gps_file, write_bin_gps_file, write_dronekit_la_output_file
from flask_login import  current_user, login_required
from werkzeug.utils import secure_filename

from ..forms import FlightForm, LogForm
from ..models import Project, Drone, Flight, Log

#####   FLIGHT MANAGEMENT ROUTES AND VIEWS
flight = Blueprint('flight', __name__)

#   VIEW ALL FLIGHTS
@flight.route('/flights')
@login_required
def view_all_flights():
    """
        Route for viewing all of the user's flights. Automatically called when user opens '/flights'
        in a web browser. Requires user login.
    """
    user = current_user

    #get projects of user
    project_ids = db.session.query(Project.id).filter_by(user_id=user.id)

    #get flights from projects
    flights = Flight.query.filter(Flight.project_id.in_(project_ids)).all()

    #get projects for flights
    for flight in flights:
        flight.project = Project.query.get(flight.project_id)

    #get drones used in flights
    for flight in flights:
        flight.drone = Drone.query.get(flight.drone_id)

    flight_count = len(flights)
    return render_template("flights.html", title="Flights", user=user, flights=flights, flight_count=flight_count)

#VIEW FLIGHT DETAILS
@flight.route('/flight/view/<flight_id>', methods=['GET','POST'])
@login_required
def view_flight(flight_id):
    """
        Route for viewing more details for a user-specified flight.
        Called when user opens '/flights/view/<flight_id>in a web browser.
        <flight_id> is a parameter for specifying which flight to open.
        Requires user login. Only the owner of the flight can view his/her flight. Will return
        404 Not Found for non-existent flight, or non-matching user credentials.
    """
    user = current_user

    #check if flight exists
    flight = Flight.query.get(flight_id)
    if flight is None:
        abort(404)

    #check if User owns the flight
    project = Project.query.get(flight.project_id)
    if current_user.id != project.user_id:
        abort(404)

    drone = Drone.query.get(flight.drone_id)
    logs = Log.query.filter_by(flight_id=flight_id).all()
    maps = []
    for log in logs:
        #load json into a dictionary
        log.processed_content = json.loads(log.content)
        log.processed_content['timestamp'] = datetime.fromtimestamp(log.processed_content['timestamp']/1000000)

        #some workaround to make maps work.
        maps.append(create_map(log.id))
        log.map = maps[len(maps)-1]

        print "Log " + log.filename + " successfully processed"

    #Initialize form for adding logs
    form = LogForm()

    if form.validate_on_submit():
        #get file handle and generate secure filename
        f = form.log_file.data
        filename = secure_filename(user.username + ' - ' + str(datetime.now()) +' - '+ f.filename)

        # attempt to get gps coordinates when uploaded file is a text dump (*.log)
        gps_name = filename.rsplit('.', 1)

        # if file is a text dump, get all lines about "GPS", else no gps file
        if gps_name[1].lower() == "log":
            gps_filename = gps_name[0] + '.csv'
            write_log_gps_file(f, gps_filename)
            f.seek(0)

        # save file
        if platform.system()=='Windows':
            f.save(os.path.join(app.config['ORIGINAL_LOG_FILE_FOLDER'], filename))
        elif platform.system()=='Linux':
            f.save(os.path.join(app.config['ORIGINAL_LOG_FILE_FOLDER_2'], filename))

        #check if file is a binary log. This check can only happen after the file has been written.
        if gps_name[1].lower() == "bin":
            gps_filename = gps_name[0] + '.csv'
            write_bin_gps_file(filename, gps_filename)

        #open dronekit-la and capture output
        processed_filename = filename.rsplit('.', 1)[0] + '.json'
        content = write_dronekit_la_output_file(filename)

        #save contents to db to avoid running dronekit-la again
        log = Log(filename, content, gps_filename, processed_filename, flight_id)

        #Commit to db and refresh page
        db.session.add(log)
        db.session.commit()
        print 'Upload Successful for file: ' + filename
        return redirect(url_for('flight.view_flight', flight_id=flight_id))

    return render_template('view_flight_hardcoded.html', title=flight.name, flight=flight, drone=drone, project=project, form=form, logs=logs, maps=maps)

#   ADD A FLIGHT
@flight.route('/flight/add', methods=['GET', 'POST'])
@login_required
def add_flight():
    """
        Route for adding flights. Called when user opens '/flight/add' in a web browser.
        Requires user login.
    """
    user = current_user
    #Get projects and drones of user since these are required.
    projects = db.session.query(Project.id, Project.name).filter_by(user_id=user.id)
    drones = db.session.query(Drone.id, Drone.name).filter_by(user_id=user.id)

    #Initialize form and add choices for project and drone
    form = FlightForm()
    form.project.choices = projects
    form.drone.choices = drones

    if form.validate_on_submit():
        #Format duration to seconds only
        duration = (form.duration_hours.data*60*60) + (form.duration_mins.data*60) + (form.duration_secs.data)

        #Initialize flight object
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

        #commit to db and return to view all flights page
        db.session.add(flight)
        db.session.commit()
        return redirect(url_for("flight.view_all_flights"))

    return render_template("flight_form.html", title="Add Flight", form_title="Add Flight", submit_value="Add Flight", name="add_flight", projects=projects, form=form)

#   EDIT FLIGHT DETAILS
@flight.route('/flight/edit/<flight_id>', methods=['GET', 'POST'])
@login_required
def edit_flight(flight_id):
    """
        Route for updating flight data. Called when user opens 'flight/edit/<flight_id>' in a
        browser window. <flight_id> is a parameter that specifies which flight to update.
        Requires user login. Returns 404 Not Found for non-existing flight, or non-matching user
        credentials.
    """

    user = current_user

    #Check if flight exists
    flight = Flight.query.get(flight_id)
    if flight is None:
        abort(404)

    #Check if User owns the flight
    project = Project.query.get(flight.project_id)
    if current_user.id != project.user_id:
        abort(404)

    #Else continue with edit
    else:
        #Render form with preset values, and add choices for project and drone
        projects = db.session.query(Project.id, Project.name).filter_by(user_id=user.id)
        drones = db.session.query(Drone.id, Drone.name).filter_by(user_id=user.id)
        form = FlightForm(obj=flight)
        form.project.choices = projects
        form.drone.choices = drones

        #Format duration from seconds to hours, minutes, seconds
        form.duration_hours.data = flight.duration/ 3600
        form.duration_mins.data = (flight.duration % 3600) / 60
        form.duration_secs.data = flight.duration % 60

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
            flight.project_id = form.project.data


            db.session.commit()
            return redirect(url_for("flight.view_all_flights"))
        return render_template("flight_form.html", title=flight.name + " - Edit Flight", form_title="Edit Flight Details", submit_value="Save Changes", name="edit_flight", projects=projects, form=form)

#   DELETE A FLIGHT
@flight.route('/flight/delete/<flight_id>')
@login_required
def delete_flight(flight_id):
    """
        Route for deleting flights. Called when user opens '/flight/delete/<flight_id>' in browser
        window. <flight_id> specifies which flight to delete.
        Requires user login. Returns 404 Not Found for non-existent flight or non-matching user
        credentials.
    """

    #Check if flight exists
    flight = Flight.query.get(flight_id)
    if flight is None:
        abort(404)

    #check if User owns the flight.
    project = Project.query.get(flight.project_id)
    if current_user.id != project.user_id:
        abort(404)

    #else continue with delete
    else:
        db.session.delete(flight)
        db.session.commit()
        return redirect(url_for("flight.view_all_flights"))
