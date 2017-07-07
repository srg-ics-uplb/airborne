
from flask import Blueprint, render_template, abort, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from app import login_manager, bcrypt, db, models
from ..forms import LoginForm, SignupForm


#####   USER MANAGEMENT ROUTES AND VIEWS   
user = Blueprint('user', __name__)






@user.route('/dashboard')
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



@user.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user.dashboard'))

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
                return redirect (url_for('user.dashboard'))

       
    return render_template('login.html', title="Sign In", form=form)



@user.route('/signup', methods=['GET','POST'])    
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('user.dashboard'))

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
        return redirect(url_for('user.login'))
    return render_template('signup.html', title='Sign up',form=form)

@user.route('/logout')
@login_required
def logout():
    user = current_user
    print current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect(url_for('general.home')) 

@login_manager.user_loader
def load_user(id):
    return models.User.query.get(id)



