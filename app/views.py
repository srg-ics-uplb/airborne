from app import app, login_manager, bcrypt, db, models
from flask import render_template, flash, redirect, session, url_for, request, g
from .forms import LoginForm, SignupForm, AddDroneForm
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
    # drones = models.Drone.query.filter_by(user_id=user.id)
    # flights = models.Post.query.filter_by(user_id=user.id)
    return render_template('dashboard.html',title='Dashboard', user=user, projects=projects)

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
    form = AddDroneForm()
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
            form.max_payload_capacity.data,
            form.max_speed.data
        )
        
        db.session.add(equipment)
        db.session.commit()

        
        return redirect(url_for('view_drones'))   
    return render_template('add_drone.html', form = form)

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