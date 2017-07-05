from app import app, login_manager, bcrypt, db, models
from flask import render_template, flash, redirect, session, url_for, request, g
from .forms import *
from flask_login import login_user, logout_user, current_user, login_required

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/dashboard')
@login_required
def dashboard():
    user = current_user
    projects = models.Project.query.filter_by(user_id=user.id)
    project_count = projects.count()
    drone_count = models.Drone.query.filter_by(user_id=user.id).count()
    flight_count = 0
    for project in projects:
        flight_count = flight_count + project.flights.count()
    
    return render_template('dashboard.html',title='Dashboard', user=user, project_count=project_count, drone_count=drone_count, flight_count= flight_count)

#####   DRONE MANAGEMENT ROUTES AND VIEWS  

#   VIEW ALL DRONES
@app.route('/drones')
@login_required
def view_all_drones():
    user = current_user
    
    drones = models.Drone.query.filter_by(user_id=user.id)
    print drones
    return render_template('drones.html', title='List of drones', user=user, drones=drones)

#   VIEW DRONE DETAILS
@app.route('/drone/view/<drone_id>')
@login_required
def view_drones(drone_id):
    user = current_user
    drone = models.Drone.query.get(drone_id)

    return render_template("view_drone.html", title=drone.name, drone=drone)
    
#   ADD A DRONE    
@app.route('/drone/add', methods=['GET','POST'])
@login_required
def add_drone():
    user = current_user
    form = DroneForm()
    if form.validate_on_submit():
        equipment = models.Drone(
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

        
        return redirect(url_for('view_all_drones'))   
    return render_template('drone_form.html', form = form, form_title="Add a Drone", name="add_drone", submit_value="Add Drone")

#   EDIT DRONE DETAILS
@app.route('/drone/edit/<drone_id>', methods=['GET','POST', 'PUT'])
@login_required
def edit_drone(drone_id):
    drone = models.Drone.query.get(drone_id)
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

        return redirect(url_for('view_all_drones'))

    return render_template("drone_form.html", title="Edit Drone", form = form, form_title="Edit Drone Details", name="edit_drone", submit_value="Save Changes")

#   DELETE A DRONE
@app.route('/drone/delete/<drone_id>')
@login_required
def delete_drone(drone_id):
    drone = models.Drone.query.get(drone_id)
    db.session.delete(drone)
    db.session.commit()
    return redirect(url_for('view_all_drones'))


#####   PROJECT MANAGEMENT ROUTES AND VIEWS    


#   VIEW ALL PROJECTS
@app.route('/projects')
@login_required
def view_all_projects():
    user = current_user
    projects = models.Project.query.filter_by(user_id=user.id)


    return render_template('projects.html', title='Projects', user=user, projects=projects)

#   VIEW A PROJECT
@app.route('/project/view/<project_id>')
@login_required
def view_project(project_id):
    user = current_user
    project = models.Project.query.get(project_id)

    return render_template("view_project.html", title=project.name, project=project)

#   ADD A PROJECT
@app.route('/project/add', methods=['GET','POST'])
@login_required
def add_project():
    user = current_user
    form = ProjectForm()
    if form.validate_on_submit():
        project = models.Project(form.name.data, form.description.data, user.get_id())
        db.session.add(project)
        db.session.commit()
        return redirect(url_for('view_all_projects'))
    
    return render_template("project_form.html", form=form, form_title="Add a Project", submit_value="Add Project", name="add_project")

#   EDIT PROJECT DETAILS
@app.route('/project/edit/<project_id>', methods=['GET','POST'])
@login_required
def edit_project(project_id):
    user = current_user
    project = models.Project.query.get(project_id)
    form = ProjectForm(obj=project)
    if form.validate_on_submit():
        project.name = form.name.data
        project.description = form.description.data
        db.session.commit()
        return redirect(url_for('view_all_projects'))
    return render_template("project_form.html", form=form, form_title="Edit Project Details", submit_value="Save Changes", name="edit_project")

#   DELETE A PROJECT
@app.route('/project/delete/<project_id>')
@login_required
def delete_project(project_id):
    project = models.Project.query.get(project_id)
    db.session.delete(project)
    db.session.commit()

    return redirect(url_for('view_all_projects'))

#####   FLIGHT MANAGEMENT ROUTES AND VIEWS

#   VIEW ALL FLIGHTS
@app.route('/flights')
@login_required
def view_all_flights():
    user = current_user
    
    #get projects of user
    project_ids = db.session.query(models.Project.id).filter_by(user_id = user.id)

    #get flights from projects
    flights = models.Flight.query.filter(models.Flight.project_id.in_(project_ids)).all()

    #get projects for flights
    for flight in flights:
        flight.project = models.Project.query.get(flight.project_id)

    #get drones used in flights
    for flight in flights:
        flight.drone = models.Drone.query.get(flight.drone_id)

    flight_count=len(flights)
    return render_template("flights.html", title="Flights", user=user, flights=flights, flight_count = flight_count)

#VIEW FLIGHT DETAILS
@app.route('/flight/view/<flight_id>')
@login_required
def view_flight(flight_id):
    user = current_user
    flight = models.Flight.query.get(flight_id)
    drone = models.Drone.query.get(flight.drone_id)
    project = models.Project.query.get(flight.project_id)

    return render_template('view_flight.html', title=flight.name,  flight=flight, drone=drone, project=project)

#   ADD A FLIGHT
@app.route('/flight/add', methods=['GET','POST'])
@login_required
def add_flight():
    user = current_user
    projects = db.session.query(models.Project.id, models.Project.name).filter_by(user_id = user.id)
    drones = db.session.query(models.Drone.id, models.Drone.name).filter_by(user_id = user.id)
    form= FlightForm()
    form.project.choices= projects
    form.drone.choices = drones

    if form.validate_on_submit():
        duration = (form.duration_hours.data*60*60)+(form.duration_mins.data*60)+(form.duration_secs.data)
        flight = models.Flight(
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
        return redirect(url_for("view_all_flights"))

    return render_template("flight_form.html", title="Add Flight", form_title="Add Flight", submit_value="Add Flight", name="add_flight", projects=projects, form=form)

#   EDIT FLIGHT DETAILS
@app.route('/flight/edit/<flight_id>', methods=['GET','POST'])
@login_required
def edit_flight(flight_id):
    user = current_user
    projects = db.session.query(models.Project.id, models.Project.name).filter_by(user_id = user.id)
    drones = db.session.query(models.Drone.id, models.Drone.name).filter_by(user_id = user.id)
    flight = models.Flight.query.get(flight_id)
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
        return redirect(url_for("view_all_flights"))
    return render_template("flight_form.html", title="Edit Flight", form_title="Edit Flight Details", submit_value="Save Changes", name="edit_flight", projects=projects, form=form)

#   DELETE A FLIGHT
@app.route('/flight/delete/<flight_id>')
@login_required
def delete_flight(flight_id):
    flight = models.Flight.query.get(flight_id)
    db.session.delete(flight)
    db.session.commit()
    return redirect(url_for("view_all_flights"))


#####   USER MANAGEMENT ROUTES AND VIEWS   

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print form.username.data
        user = models.User.query.filter_by(username=form.username.data).first()
        print user
        
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                print 'yay'
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=form.remember_me.data)
                return redirect (url_for('dashboard'))

       
    return render_template('login.html', title="Sign In", form=form)



@app.route('/signup', methods=['GET','POST'])    
def signup():
    
    form = SignupForm()

    if form.validate_on_submit():

        user = models.User(
        form.firstname.data,
        form.middlename.data,
        form.lastname.data,
        form.email.data, 
        form.username.data, 
        bcrypt.generate_password_hash(form.password.data), 
        form.age.data,
        form.sex.data
        )
        

        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html', title='Sign up',form=form)

@app.route('/logout')
@login_required
def logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect(url_for('home')) 

@login_manager.user_loader
def load_user(id):
    return models.User.query.get(id)