"""
    Views module for Projects. This contains routes and functions that are project-related.
"""
from app import db
from flask import render_template, redirect, url_for, abort, Blueprint
from flask_login import  current_user, login_required
from ..forms import ProjectForm
from ..models import Project



#####   PROJECT MANAGEMENT ROUTES AND VIEWS

project = Blueprint('project', __name__)

#   VIEW ALL PROJECTS
@project.route('/projects')
@login_required
def view_all_projects():
    """
        Route for viewing all projects of the user. Called when user opens '/projects'
        Requires user login.
    """
    user = current_user

    #Get all of user's projects
    projects = Project.query.filter_by(user_id=user.id)


    return render_template('projects.html', title='Projects', user=user, projects=projects)

#   VIEW A PROJECT
@project.route('/project/view/<project_id>')
@login_required
def view_project(project_id):
    """
        Route for viewing a specific project. Called when user opens '/project/view/<project_id>
        in a web browser. <project_id> is a parameter that specifies which project to view.
        Requires user login.  Returns 404 Not Found if project is non-existent, or non-matching
        user credentials.
    """
    #Check if project exists
    project = Project.query.get(project_id)
    if project is None:
        abort(404)
    #Check if user owns the project
    elif current_user.id != project.user_id:
        abort(404)

    #Else proceed to view
    else:
        return render_template("view_project.html", title=project.name, project=project)

#   ADD A PROJECT
@project.route('/project/add', methods=['GET', 'POST'])
@login_required
def add_project():
    """
        Route for adding a new project. Called when user opens '/project/add' in a web browser.
        Requires user login.
    """
    user = current_user
    #Generate form
    form = ProjectForm()
    if form.validate_on_submit():
        #Create new Project object
        project = Project(form.name.data, form.description.data, user.get_id())

        #Commit to db and redirect back to projects page
        db.session.add(project)
        db.session.commit()
        return redirect(url_for('project.view_all_projects'))

    return render_template("project_form.html", form=form, form_title="Add a Project", submit_value="Add Project", name="add_project")

#   EDIT PROJECT DETAILS
@project.route('/project/edit/<project_id>', methods=['GET', 'POST'])
@login_required
def edit_project(project_id):
    """
        Route for editing project details. Called when user opens '/project/edit/<project_id>'
        in a web browser. <project_id> is a parameter that specifies which project to edit.
        Requires user login. Returns 404 Not Found if project is non-existent, or non-matching
        user credentials.
    """
    #Check if project exists
    project = Project.query.get(project_id)
    if project is None:
        abort(404)

    #Check if user owns project
    elif current_user.id != project.user_id:
        abort(404)
    #Else proceed to edit
    else:
        #Initialize form with values
        form = ProjectForm(obj=project)
        if form.validate_on_submit():
            #Replace old values with new ones
            project.name = form.name.data
            project.description = form.description.data
            #Commit changes to db and redirect back to projects page
            db.session.commit()
            return redirect(url_for('project.view_all_projects'))
        return render_template("project_form.html", form=form, form_title="Edit Project Details", submit_value="Save Changes", name="edit_project")

#   DELETE A PROJECT
@project.route('/project/delete/<project_id>')
@login_required
def delete_project(project_id):
    """
        Route for deleting a project. Called when user opens '/project/delete/<project_id>'
        in a web browser. <project_id> is a parameter that specifies which project to delete.
        Requires user login. Returns 404 Not Found if project is non-existent, or non-matching
        user credentials.
    """
    #Check if project exists
    project = Project.query.get(project_id)
    if project is None:
        abort(404)
    #Check if user owns project
    elif current_user.id != project.user_id:
        abort(404)
    #Proceed to delete
    else:
        #Commit changes and redirect back to projects page
        db.session.delete(project)
        db.session.commit()
        return redirect(url_for('project.view_all_projects'))
