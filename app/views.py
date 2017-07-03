from app import app, login_manager, bcrypt, db, models
from flask import render_template, flash, redirect, session, url_for, request, g
from .forms import LoginForm, SignupForm, DroneForm, ProjectForm
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

@app.route('/drones')
@login_required
def view_drones():
    user = current_user
    
    drones = models.Drone.query.filter_by(user_id=user.id)
    print drones
    return render_template('drones.html', title='List of drones', user=user, drones=drones)


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

        
        return redirect(url_for('view_drones'))   
    return render_template('drone_form.html', form = form, form_title="Add a Drone", name="add_drone", submit_value="Add Drone")

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

        return redirect(url_for('view_drones'))

    return render_template("drone_form.html", title="Edit Drone", form = form, form_title="Edit Drone Details", name="edit_drone", submit_value="Save Changes")

@app.route('/drone/delete/<drone_id>')
@login_required
def delete_drone(drone_id):
    drone = models.Drone.query.get(drone_id)
    db.session.delete(drone)
    db.session.commit()
    return redirect(url_for('view_drones'))


#####   PROJECT MANAGEMENT ROUTES AND VIEWS    

@app.route('/projects')
@login_required
def view_projects():
    user = current_user
    projects = models.Project.query.filter_by(user_id=user.id)


    return render_template('projects.html', title='Projects', user=user, projects=projects)

@app.route('/project/add', methods=['GET','POST'])
@login_required
def add_project():
    user = current_user
    form = ProjectForm()
    if form.validate_on_submit():
        project = models.Project(form.name.data, form.description.data, user.get_id())
        db.session.add(project)
        db.session.commit()
        return redirect(url_for('view_projects'))
    
    return render_template("project_form.html", form=form, form_title="Add a Project", submit_value="Add Project", name="add_project")

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
        return redirect(url_for('view_projects'))
    return render_template("project_form.html", form=form, form_title="Edit Project Details", submit_value="Save Changes", name="edit_project")

@app.route('/project/delete/<project_id>')
@login_required
def delete_project(project_id):
    project = models.Project.query.get(project_id)
    db.session.delete(project)
    db.session.commit()

    return redirect(url_for('view_projects'))

#####   FLIGHT MANAGEMENT ROUTES AND VIEWS
@app.route('/flights')
@login_required
def view_flights():
    user = current_user
    projects = db.session.query(models.Project.id).filter_by(user_id = user.id)
    flights = models.Flight.query.filter(models.Flight.project_id.in_(projects)).all()
    flight_count=len(flights)
    return render_template("flights.html", title="Flights", user=user, flights=flights, flight_count = flight_count)

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