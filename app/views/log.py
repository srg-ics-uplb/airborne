"""
    View module for Logs. This module defines functions required for log upload, analysis, and processing.
"""
import os
import csv
import subprocess
import platform
from math import sin, cos, radians, sqrt, atan2
from app import db, app
from flask import redirect, url_for, abort, Blueprint
from flask_login import  current_user, login_required
from flask_googlemaps import Map
from ..models import Project, Flight, Log
##### LOG MANAGEMENT ROUTES AND VIEWS
log = Blueprint('log', __name__)



@log.route('/log/delete/<log_id>', methods=['GET', 'DELETE'])
@login_required
def delete_log(log_id):
    """
        Route for deleting logs. Called when user enters '/log/delete/<log_id>' in the browser
        window. <log_id> is the parameter used to identify the log file to be deleted.
        Requires user login. Returns 404 for non-existent log file, 
        or non-matching user credentials.
    """
    #Check if log exists
    log = Log.query.get(log_id)
    if log is None:
        abort(404)

    #Check if user owns the log file
    flight_id = log.flight_id
    flight = Flight.query.get(flight_id)
    project = Project.query.get(flight.project_id)
    if current_user.id != project.user_id:
        abort(404)
    #Else proceed to delete file
    else:
        #remove original log file
        os.remove(os.path.join(app.config['ORIGINAL_LOG_FILE_FOLDER'], log.filename))

        #remove gps csv file if exists
        if log.gps_filename is not None:
            os.remove(os.path.join(app.config['GPS_COORDINATE_FILE_FOLDER'], log.gps_filename))

        #remove processed dronekit-la output file
        os.remove(os.path.join(app.config['PROCESSED_OUTPUT_FILE_FOLDER'], log.processed_filename))

        #remove from db and redirect to flight page
        db.session.delete(log)
        db.session.commit()
        return redirect(url_for('flight.view_flight', flight_id=flight_id))

def write_dronekit_la_output_file(filename):
    """
        Write JSON file for dronekit-la output
    """
    if platform.system()=='Windows': #if running on windows system
        #run dronekit-la
        args = app.config['LOG_ANALYZER_DIR'] + app.config['ORIGINAL_LOG_FILE_FOLDER'] + '\\' + filename
        content = subprocess.check_output(args)

        #open a file handle and save output of dronekit-la to a json file
        processed_filename = filename.rsplit('.', 1)[0] + '.json'
        with open(app.config['PROCESSED_OUTPUT_FILE_FOLDER'] + '\\' + processed_filename, 'w') as processed:
            processed.write(content)
            processed.close()
    elif platform.system()=='Linux': #if running on linux system
        #run dronekit-la
        args = app.config['LOG_ANALYZER_DIR_2'] + app.config['ORIGINAL_LOG_FILE_FOLDER'] + '\\' + filename
        content = subprocess.check_output(args)

        #open a file handle and save output of dronekit-la to a json file
        processed_filename = filename.rsplit('.', 1)[0] + '.json'
        with open(app.config['PROCESSED_OUTPUT_FILE_FOLDER'] + '\\' + processed_filename, 'w') as processed:
            processed.write(content)
            processed.close()

    #return the contents of the file in case content needs to be saved to db
    return content

def write_dronekit_la_output_file_plain(filename):
    """
        Write plain text file for dronekit-la output
    """
    if platform.system()=='Windows': #if running on windows system
        #run dronekit-la
        args = app.config['LOG_ANALYZER_TXT_DIR'] + app.config['ORIGINAL_LOG_FILE_FOLDER'] + '\\' + filename
        content = subprocess.check_output(args)

        #open file handle and save output to txt file
        processed_filename = filename.rsplit('.', 1)[0] + '.txt'
        filepath = app.config['PROCESSED_OUTPUT_FILE_FOLDER'] + '\\' + processed_filename
        with open(filepath, 'w') as processed:
            processed.write(content)
            processed.close()
    
    elif platform.system()=='Linux': #if running on linux system
        #run dronekit-la
        args = app.config['LOG_ANALYZER_TXT_DIR_2'] + app.config['ORIGINAL_LOG_FILE_FOLDER'] + '\\' + filename
        content = subprocess.check_output(args)

        #open file handle and save output to txt file
        processed_filename = filename.rsplit('.', 1)[0] + '.txt'
        filepath = app.config['PROCESSED_OUTPUT_FILE_FOLDER'] + '\\' + processed_filename
        with open(filepath, 'w') as processed:
            processed.write(content)
            processed.close()


    #return contents in case content needs to be saved to db
    return content


def write_log_gps_file(file_handle, filename):
    """
        Write CSV file for GPS data from dataflash text dumps(*.log)
    """
    #open file handle for gps csv file
    g = open(app.config['GPS_COORDINATE_FILE_FOLDER']+'\\'+ filename, 'w')

    #write initial row containing columns
    g.write('TimeUS,Status,GMS,GWk,NSats,HDop,Lat,Lng,RAlt,Alt,Spd,GCrs,VZ,U\n')

    #traverse lines of uploaded text dump
    for line in file_handle:
        a = line.split(', ', 1)

        #pick only lines starting with GPS
        if a[0] == "GPS":
            #remove carriage returns and whitespace, then write to file
            b = a[1].replace('\r', '')
            b = b.replace(' ', '')
            g.write(b)
    g.close()

    #return file handle to beginning of file
    file_handle.seek(0)

def write_bin_gps_file(log, filename):
    """
        Write CSV file for GPS data from dataflash binary logs(*.bin)
    """
    #run mavlogdump.py
    if platform.system()=='Windows': 
        args = app.config['MAVLOGDUMP_RUN'] + '\\' + log
    elif platform.system()=='Linux':
        args = app.config['MAVLOGDUMP_RUN_2'] + '\\' + log
    content = subprocess.check_output(args)

    #save contents to a csv file
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
    #get starting point and markers
    point = get_first_point(log_id)
    markers = get_map_markers_json(log_id)

    #draw polyline
    polyline = {
        'stroke_color': '#0AB0DE',
        'stroke_opacity': 1.0,
        'stroke_weight': 3,
        'path': markers
    }

    #return Map object
    return Map(
        identifier="map" + str(log_id),
        zoom=15,
        lat=point[0],
        lng=point[1],
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
        basepoint = line['Lat'], line['Lng']
    return basepoint


def get_map_markers_json(log_id):
    """
        This function attempts to get a good amount of markers for google maps to render.
        If the approximate distance between two points is greater than a certain threshold,
        add a new waypoint. This is to avoid having two much points to render.
    """
    #set hardcoded threshold
    threshold = 2.5
    waypoints = []

    #retrieve log file
    log = Log.query.get(log_id)
    filepath = app.config['GPS_COORDINATE_FILE_FOLDER'] + '\\' + log.gps_filename
    with open(filepath, 'r') as mapfile:
        #initialize DictReader
        reader = csv.DictReader(mapfile)

        #move to next line and set first point as first waypoint
        line = reader.next()
        #starting waypoint uses a green marker, with "START" in infobox
        waypoint = {
            'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
            'lat': float(line['Lat']),
            'lng': float(line['Lng']),
            'infobox': '<p> START </p>'
        }
        prev = waypoint

        waypoints.append(waypoint)
        count = 1

        #for the remaining lines, calculate distance from previous waypoint
        for row in reader:
            d = calc_distance(row, prev)

            #if distance is greater than set threshold, set current point
            #as new previous point
            #
            if d > threshold:
                #normal waypoints have blue markers, with count in infobox
                prev = {
                    'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
                    'lat': float(row['Lat']),
                    'lng': float(row['Lng']),
                    'infobox': '<p> '+ str(count) +' </p>'
                }

                #append previous point to list of waypoints and increment count
                waypoints.append(prev)
                count += 1
        #final waypoint has a red marker, with "END" in infobox
        waypoints[len(waypoints)-1]['icon'] = 'http://maps.google.com/mapfiles/ms/icons/red-dot.png'
        waypoints[len(waypoints)-1]['infobox'] = '<p> END </p>'

    return waypoints

def calc_distance(point1, point2):
    """
        Distance calculation between two points' coordinates(Latitude and Longitude)
        Formula from http://www.movable-type.co.uk/scripts/latlong.html
    """
    #row is point1
    #prev is point2
    radius = 6371e3
    phi1 = radians(float(point1['Lat']))
    phi2 = radians(float(point2['lat']))
    deltaphi = radians(float(point1['Lat']) - float(point2['lat']))
    deltalambda = radians(float(point1['Lng']) - float(point2['lng']))
    a = sin(deltaphi/2) * sin(deltaphi/2) + (cos(phi1) * cos(phi2) * sin(deltalambda/2) * sin(deltalambda/2))
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = radius * c
    return distance
