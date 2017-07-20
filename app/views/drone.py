"""
    View module for Drones. This module defines routes and logic for Drone-related things.
"""

from app import db
from flask import render_template, redirect, url_for, abort, Blueprint
from flask_login import current_user, login_required
from ..forms import DroneForm
from ..models import Drone


#####   DRONE MANAGEMENT ROUTES AND VIEWS

drone = Blueprint('drone', __name__)

#   VIEW ALL DRONES
@drone.route('/drones')
@login_required
def view_all_drones():
    """
        Route for retrieving all of the user's drones. Called when user opens '/drones'
        in a web browser. Requires user login.
    """
    user = current_user

    #get all drones owned by the user
    drones = Drone.query.filter_by(user_id=user.id)
    return render_template('drones.html', title='List of drones', user=user, drones=drones)

#   VIEW DRONE DETAILS
@drone.route('/drone/view/<drone_id>')
@login_required
def view_drones(drone_id):
    """
        Route for viewing details of a specific user-specified drone.
        Called when user opens '/drone/view/<drone_id>'. <drone_id> is a parameter
        for identifying which drone to view. Requires user login.
        Returns 404 Not Found for non-existent drone, or non-matching user credentials.
    """
    #Check if drone exists
    drone = Drone.query.get(drone_id)
    if drone is None:
        abort(404)
    #Check if user owns the drone
    elif current_user.id != drone.user_id:
        abort(404)

    #Else proceed to view
    else:
        return render_template("view_drone.html", title=drone.name, drone=drone)

#   ADD A DRONE
@drone.route('/drone/add', methods=['GET', 'POST'])
@login_required
def add_drone():
    """
        Route for adding a new drone. Called when user opens '/drone/add' in a web browser.
        Requires user login.
    """
    user = current_user

    #initialize form
    form = DroneForm()
    if form.validate_on_submit():
        #create new drone object
        equipment = Drone(
            form.name.data,
            form.weight.data,
            form.version_number.data,
            form.brand.data,
            form.model.data,
            form.notes.data,
            'drone',
            user.get_id(),
            form.max_payload_cap.data,
            form.max_speed.data
        )
        #commit to db
        db.session.add(equipment)
        db.session.commit()

        #return to view all drones page
        return redirect(url_for('drone.view_all_drones'))
    return render_template('drone_form.html', form=form, form_title="Add a Drone", name="add_drone", submit_value="Add Drone")

#   EDIT DRONE DETAILS
@drone.route('/drone/edit/<drone_id>', methods=['GET', 'POST', 'PUT'])
@login_required
def edit_drone(drone_id):
    """
        Route for editing drone details. Called when user opens '/drone/edit/<drone_id>' in a
        web browser. Requires user login. Returns 404 Not Found if drone is non-existent,
        or not matching user credentials.
    """
    #Check if drone exists
    drone = Drone.query.get(drone_id)
    if drone is None:
        abort(404)
    #Check if user owns the drone
    elif current_user.id != drone.user_id:
        abort(404)

    #Else proceed to edit
    else:
        form = DroneForm(obj=drone)

        if form.validate_on_submit():
            drone.name = form.name.data
            drone.weight = form.weight.data
            drone.version_number = form.version_number.data
            drone.brand = form.brand.data
            drone.model = form.model.data
            drone.notes = form.notes.data
            drone.max_payload_cap = form.max_payload_cap.data
            drone.max_speed = form.max_speed.data

            print form.name.data
            db.session.commit()

            return redirect(url_for('drone.view_all_drones'))

        return render_template("drone_form.html", title="Edit Drone", form=form, form_title="Edit Drone Details", name="edit_drone", submit_value="Save Changes")

#   DELETE A DRONE
@drone.route('/drone/delete/<drone_id>')
@login_required
def delete_drone(drone_id):
    """
        Route for deleting a drone. Called when user opens '/drone/delete/<drone_id>'
        in a browser. Requires user login. Returns 404 Not Found if drone is
        non-existent, or non-matching user credentials.
    """
    #Check if drone exists
    drone = Drone.query.get(drone_id)
    if drone is None:
        abort(404)
    #Check if user owns the drone
    elif current_user.id != drone.user_id:
        abort(404)

    #Else proceed to delete
    else:
        db.session.delete(drone)
        db.session.commit()
        #return to view all drones page
        return redirect(url_for('drone.view_all_drones'))
