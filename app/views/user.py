"""
    Views module for Users. This contains routes and functions that are user-related.
"""
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from app import login_manager, bcrypt, db
from ..forms import LoginForm, SignupForm
from ..models import Project, Drone, User


#####   USER MANAGEMENT ROUTES AND VIEWS
user = Blueprint('user', __name__)

@user.route('/dashboard')
@login_required
def dashboard():
    """
        User dashboard. Presents brief information for user.
        Called when user opens '/dashboard'.
        Requires user login.
    """
    #Get user's project, flight, and drone counts.
    user = current_user
    projects = Project.query.filter_by(user_id=user.id)
    project_count = projects.count()
    drone_count = Drone.query.filter_by(user_id=user.id).count()
    flight_count = 0
    for project in projects:
        flight_count = flight_count + project.flights.count()

    return render_template('dashboard.html', title='Dashboard', user=user, project_count=project_count, drone_count=drone_count, flight_count=flight_count)



@user.route('/login', methods=['GET', 'POST'])
def login():
    """
        Login page for users. Called when user opens '/login'
        If user is currently logged in, user is redirected to dashboard instead.
    """
    #Check if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for('user.dashboard'))
    #Generate login form
    form = LoginForm()
    if form.validate_on_submit():
        print form.username.data
        #Check if user exists
        user = User.query.filter_by(username=form.username.data).first()
        print user

        if user:
            #Check if passwords match
            if bcrypt.check_password_hash(user.password, form.password.data):
                #Proceed with login and redirect to dashboard
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=form.remember_me.data)
                return redirect(url_for('user.dashboard'))
    return render_template('login.html', title="Sign In", form=form)



@user.route('/signup', methods=['GET', 'POST'])
def signup():
    """
        Signup for new users. Called when user opens '/signup'
        If user is currently logged in, user is redirected to dashboard instead.
    """
    #Check if there's a user currently logged in
    if current_user.is_authenticated:
        return redirect(url_for('user.dashboard'))

    #Initialize signup form
    form = SignupForm()
    if form.validate_on_submit():
        #Create new User object
        user = User(
            form.firstname.data,
            form.middlename.data,
            form.lastname.data,
            form.email.data,
            form.username.data,
            bcrypt.generate_password_hash(form.password.data),
            form.age.data,
            form.sex.data
        )

        #Add new user to database and redirect to log in page
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('user.login'))
    return render_template('signup.html', title='Sign up', form=form)

@user.route('/logout')
@login_required
def logout():
    """
        Route for user logout. Logs out current user upon opening '/logout'
        Requires user login.
    """
    user = current_user
    print current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect(url_for('general.home'))

@login_manager.user_loader
def load_user(id):
    """
        Required user loader for flask_login's login_manager module
    """
    return User.query.get(id)
