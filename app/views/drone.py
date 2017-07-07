from app import db
from flask import render_template, redirect, url_for, request, abort, Blueprint
from ..forms import DroneForm
from ..models import Drone
from flask_login import  current_user, login_required

#####   DRONE MANAGEMENT ROUTES AND VIEWS  

drone = Blueprint ('drone', __name__)

#   VIEW ALL DRONES
@drone.route('/drones')
@login_required
def view_all_drones():
    user = current_user
    
    drones = Drone.query.filter_by(user_id=user.id)
    return render_template('drones.html', title='List of drones', user=user, drones=drones)

#   VIEW DRONE DETAILS
@drone.route('/drone/view/<drone_id>')
@login_required
def view_drones(drone_id):
    drone = Drone.query.get(drone_id)
    if drone is None:
        abort(404)
    elif current_user.id != drone.user_id:
        abort(404)
    
    else:
        return render_template("view_drone.html", title=drone.name, drone=drone)
    
#   ADD A DRONE    
@drone.route('/drone/add', methods=['GET','POST'])
@login_required
def add_drone():
    user = current_user
    form = DroneForm()
    if form.validate_on_submit():
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
        
        db.session.add(equipment)
        db.session.commit()

        
        return redirect(url_for('drone.view_all_drones'))   
    return render_template('drone_form.html', form = form, form_title="Add a Drone", name="add_drone", submit_value="Add Drone")

#   EDIT DRONE DETAILS
@drone.route('/drone/edit/<drone_id>', methods=['GET','POST', 'PUT'])
@login_required
def edit_drone(drone_id):
    drone = Drone.query.get(drone_id)
    if drone is None:
        abort(404)
    elif current_user.id != drone.user_id:
        abort(404)
    
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

        return render_template("drone_form.html", title="Edit Drone", form = form, form_title="Edit Drone Details", name="edit_drone", submit_value="Save Changes")

#   DELETE A DRONE
@drone.route('/drone/delete/<drone_id>')
@login_required
def delete_drone(drone_id):
    drone = Drone.query.get(drone_id)
    if drone is None:
        abort(404)
    elif current_user.id != drone.user_id:
        abort(404)
    
    else:
        db.session.delete(drone)
        db.session.commit()
        return redirect(url_for('drone.view_all_drones'))

