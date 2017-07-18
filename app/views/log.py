from app import db, app
from flask import redirect, render_template, url_for, abort, Blueprint
from flask_login import  current_user, login_required
from ..models import Project, Flight, Log
from werkzeug.utils import secure_filename
from datetime import datetime
import os, csv
from math import sin, cos, radians, sqrt, atan2
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

def get_first_point(log_id):
    log = Log.query.get(log_id)
    filepath = app.config['GPS_COORDINATE_FILE_FOLDER'] + '\\' + log.gps_filename
    with open(filepath, 'r') as mapfile:
        reader = csv.DictReader(mapfile)
        line = reader.next()
        basepoint = line['Lat'], line['Lng']
    return basepoint

def get_map_markers(log_id):
    """
        This function attempts to get a good amount of markers for google maps to render
        If the approximate distance between two points is greater than a certain threshold,
        add a new waypoint. This is to avoid having two much points to render.
        Formula from http://www.movable-type.co.uk/scripts/latlong.html
    """
    threshold = 3
    r = 6371e3
    waypoints = []
    log = Log.query.get(log_id)
    filepath = app.config['GPS_COORDINATE_FILE_FOLDER'] + '\\' + log.gps_filename
    with open(filepath, 'r') as mapfile:
        reader = csv.DictReader(mapfile)
        line = reader.next()
        waypoint = line['Lat'], line['Lng']
        prev = waypoint

        print prev
        waypoints.append(waypoint)
        for row in reader:
            phi1 = radians(float(row['Lat']))
            phi2 = radians(float(prev[0]))
            deltaphi = radians(float(row['Lat']) - float(prev[0]))
            deltalambda = radians(float(row['Lng']) - float(prev[1]))
            a = sin(deltaphi/2) * sin(deltaphi/2) + (cos(phi1) * cos(phi2) * sin(deltalambda/2) * sin(deltalambda/2))
            c = 2 * atan2(sqrt(a),sqrt(1-a))
            d = r * c

            
            if d > threshold:
                prev = row['Lat'], row['Lng']
                waypoints.append(prev)
            
    return waypoints


def get_map_markers_json(log_id):
    """
        Same as get_map_markers, but output is in json format
    """
    threshold = 3
    r = 6371e3
    waypoints = []
    log = Log.query.get(log_id)
    filepath = app.config['GPS_COORDINATE_FILE_FOLDER'] + '\\' + log.gps_filename
    with open(filepath, 'r') as mapfile:
        reader = csv.DictReader(mapfile)
        line = reader.next()
        waypoint = {
            'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
            'lat': float(line['Lat']),
            'lng': float(line['Lng']),
            'infobox': '<p> START </p>'
        }
        prev = waypoint

        print prev
        waypoints.append(waypoint)
        count = 1
        for row in reader:
            phi1 = radians(float(row['Lat']))
            phi2 = radians(float(prev['lat']))
            deltaphi = radians(float(row['Lat']) - float(prev['lat']))
            deltalambda = radians(float(row['Lng']) - float(prev['lng']))
            a = sin(deltaphi/2) * sin(deltaphi/2) + (cos(phi1) * cos(phi2) * sin(deltalambda/2) * sin(deltalambda/2))
            c = 2 * atan2(sqrt(a),sqrt(1-a))
            d = r * c

            
            if d > threshold:
                prev = {
                    'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
                    'lat': float(row['Lat']),
                    'lng': float(row['Lng']),
                    'infobox': '<p> '+ str(count) +' </p>'
                }
                waypoints.append(prev)
                count+=1
        waypoints[len(waypoints)-1]['icon'] = 'http://maps.google.com/mapfiles/ms/icons/red-dot.png'
        waypoints[len(waypoints)-1]['infobox'] = '<p> END </p>'
    print waypoints
    return waypoints