from app import db, app
from flask import redirect, render_template, url_for, abort, Blueprint
from flask_login import  current_user, login_required
from ..models import Project, Flight, Log
from werkzeug.utils import secure_filename
from datetime import datetime
from flask_googlemaps import Map
import os, csv, subprocess
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

def write_dronekit_la_output_file(filename):
    """
        Write JSON file for dronekit-la output
    """
    args = app.config['LOG_ANALYZER_DIR'] + app.config['ORIGINAL_LOG_FILE_FOLDER'] + '\\' + filename
    content = subprocess.check_output(args)
    

    processed_filename = filename.rsplit('.', 1)[0] + '.json'
    with open(app.config['PROCESSED_OUTPUT_FILE_FOLDER'] + '\\' + processed_filename, 'w') as processed:
        processed.write(content)
        processed.close()
    
    return content

def write_log_gps_file(file_handle, filename):
    """
        Write CSV file for GPS data from dataflash text dumps(*.log)
    """
    g = open(app.config['GPS_COORDINATE_FILE_FOLDER']+'\\'+ filename, 'w')
    g.write('TimeUS,Status,GMS,GWk,NSats,HDop,Lat,Lng,RAlt,Alt,Spd,GCrs,VZ,U\n')
    for line in file_handle:
        a = line.split(', ', 1)
        if a[0] == "GPS":
            b = a[1].replace('\r', '')
            b = b.replace(' ', '')
            g.write(b)
    g.close()
    file_handle.seek(0)

def write_bin_gps_file(log, filename):
    """
        Write CSV file for GPS data from dataflash binary logs(*.bin)
    """    
    args = app.config['MAVLOGDUMP_RUN'] + '\\' + log
    
    print args
    content = subprocess.check_output(args)
    filepath = app.config['GPS_COORDINATE_FILE_FOLDER'] + '\\' + filename
    with open(filepath, 'w') as csvfile:
        for row in content.splitlines():
            csvfile.write(row)
            csvfile.write('\n')

def create_map(log_id):
    """
        Given the log file's id, a Map object is constructed by getting the necessary waypoints
        and inserting them into the Map constructor provided by Flask-GoogleMaps
    """
    point = get_first_point(log_id)
    markers = get_map_markers_json(log_id)
    
    polyline = {
        'stroke_color': '#0AB0DE',
        'stroke_opacity': 1.0,
        'stroke_weight': 3,
        'path': get_map_markers_json(log_id)
    }

    return Map(
            identifier = "map" + str(log_id),
            zoom=15,
            lat = point[0],
            lng = point[1],
            markers=markers,
            polylines=[polyline]
        )

def get_first_point(log_id):
    """
        Get the first point from the GPS data file. 
    """
    log = Log.query.get(log_id)
    filepath = app.config['GPS_COORDINATE_FILE_FOLDER'] + '\\' + log.gps_filename
    with open(filepath, 'r') as mapfile:
        reader = csv.DictReader(mapfile)
        line = reader.next()
        print line
        basepoint = line['Lat'], line['Lng']
    return basepoint


#MAY BE REMOVED
def get_map_markers(log_id):
    """
        This function attempts to get a good amount of markers for google maps to render.
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