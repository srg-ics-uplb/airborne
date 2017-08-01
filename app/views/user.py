"""
    Views module for Users. This contains routes and functions that are user-related.
"""
from datetime import date, timedelta
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from app import login_manager, bcrypt, db
from ..forms import LoginForm, SignupForm
from ..models import Project, Drone, User,Flight


#####   USER MANAGEMENT ROUTES AND VIEWS
user = Blueprint('user', __name__)


def getMonday(date):
    print date.weekday()
    while date.weekday()!=0:
        date -= timedelta(days = 1)
    print 'date reset to nearest monday'
    return date

def getSunday(date):
    while date.weekday()!=6:
        date += timedelta(days = 1)
    return date

def getFlightsperWeek(date):
    date = getMonday(date)
    week = {}
    count = 0
    while count<=6:
        flights = Flight.query.filter(Flight.date==date).all()
        week[date] = flights
        date += timedelta(days=1)
        count += 1 
    return week

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
    drones = Drone.query.filter_by(user_id=user.id)
    current_date = date.today()
    total_project_count = projects.count()
    unused_drone_count = 0
    total_drone_count = drones.count()
    for drone in drones:
        if drone.flights.count() == 0:
            unused_drone_count += 1



    #Flight statistics
    unfinished_project_count = 0
    total_flight_count = 0
    scheduled_flights = 0
    ongoing_flights = 0
    total_flight_duration = 0
    total_flight_distance = 0
    for project in projects:
        total_flight_count = total_flight_count + project.flights.count()
        scheduled_flights =+ project.flights.filter(Flight.date>current_date).count()
        ongoing_flights =+ project.flights.filter(Flight.date==current_date).count()
        for flight in project.flights:
            if flight.date > current_date:
                unfinished_project_count += 1
                break

    finished_project_count = total_project_count - unfinished_project_count

    for project in projects:
        for flight in project.flights:
            #count only finished flights
            if flight.date<current_date:
                total_flight_duration += flight.duration
                total_flight_distance += flight.travelled_distance

    finished_flights = total_flight_count - (scheduled_flights+ongoing_flights)
    if total_flight_count==0:
        avg_flight_duration = 0
        avg_flight_distance = 0
    else:
        avg_flight_duration = total_flight_duration / total_flight_count
        avg_flight_distance = total_flight_distance / total_flight_count

    used_drone_count = total_drone_count - unused_drone_count

    if used_drone_count==0:
        avg_drone_distance = 0
        avg_drone_duration = 0
    else:
        avg_drone_distance = total_flight_distance / used_drone_count
        avg_drone_duration = total_flight_duration / used_drone_count
    
    weekly_flights = getFlightsperWeek(current_date)
    week_start = getMonday(current_date)
    week_end = getSunday(current_date)
    return render_template('dashboard.html',
                           title='Dashboard',
                           user=user,
                           total_project_count=total_project_count,
                           unfinished_project_count=unfinished_project_count,
                           finished_project_count=finished_project_count,
                           total_drone_count=total_drone_count,
                           total_flight_count=total_flight_count,
                           unused_drone_count=unused_drone_count,
                           used_drone_count=used_drone_count,
                           scheduled_flights=scheduled_flights,
                           ongoing_flights=ongoing_flights,
                           finished_flights=finished_flights,
                           total_flight_duration=total_flight_duration,
                           total_flight_distance=total_flight_distance,
                           avg_flight_distance=avg_flight_distance,
                           avg_flight_duration=avg_flight_duration,
                           avg_drone_distance=avg_drone_distance,
                           avg_drone_duration=avg_drone_duration,
                           weekly_flights=weekly_flights,
                           week_start=week_start,
                           week_end=week_end
                          )



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
    return render_template('login.html', title="Log In", form=form)



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
    return render_template('signup.html', title='Sign Up', form=form)

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
