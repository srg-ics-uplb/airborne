from app import db
from flask import render_template, redirect, url_for, request, abort, Blueprint
from ..forms import ProjectForm
from ..models import Project
from flask_login import  current_user, login_required


#####   PROJECT MANAGEMENT ROUTES AND VIEWS    

project = Blueprint('project', __name__)

#   VIEW ALL PROJECTS
@project.route('/projects')
@login_required
def view_all_projects():
    user = current_user
    projects = Project.query.filter_by(user_id=user.id)


    return render_template('projects.html', title='Projects', user=user, projects=projects)

#   VIEW A PROJECT
@project.route('/project/view/<project_id>')
@login_required
def view_project(project_id):
    user = current_user
    project = Project.query.get(project_id)
    if project is None:
        abort(404)
    elif current_user.id != project.user_id:
        abort(404)
    
    else:
        return render_template("view_project.html", title=project.name, project=project)

#   ADD A PROJECT
@project.route('/project/add', methods=['GET','POST'])
@login_required
def add_project():
    user = current_user
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(form.name.data, form.description.data, user.get_id())
        db.session.add(project)
        db.session.commit()
        return redirect(url_for('project.view_all_projects'))
    
    return render_template("project_form.html", form=form, form_title="Add a Project", submit_value="Add Project", name="add_project")

#   EDIT PROJECT DETAILS
@project.route('/project/edit/<project_id>', methods=['GET','POST'])
@login_required
def edit_project(project_id):
    user = current_user
    project = Project.query.get(project_id)
    
    if project is None:
        abort(404)
    elif current_user.id != project.user_id:
        abort(404)
    
    else:
        form = ProjectForm(obj=project)
        if form.validate_on_submit():
            project.name = form.name.data
            project.description = form.description.data
            db.session.commit()
            return redirect(url_for('project.view_all_projects'))
        return render_template("project_form.html", form=form, form_title="Edit Project Details", submit_value="Save Changes", name="edit_project")

#   DELETE A PROJECT
@project.route('/project/delete/<project_id>')
@login_required
def delete_project(project_id):
    project = Project.query.get(project_id)
    if project is None:
        abort(404)
    elif current_user.id != project.user_id:
        abort(404)
    
    else:
        db.session.delete(project)
        db.session.commit()
        return redirect(url_for('project.view_all_projects'))
