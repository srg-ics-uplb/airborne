
##### LOG MANAGEMENT ROUTES AND VIEWS


#   SUPPOSEDLY LOG UPLOAD ROUTE BUT DOESN'T WORK
@app.route('/upload', methods=['POST'])
@login_required
def upload_log(f,flight):
    filename = secure_filename(user.username + f.filename)
        
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    return redirect(url_for('view_flight', flight_id=flight.flight_id))

@app.route('/log/delete/<log_id>', methods=['GET','DELETE'])
@login_required
def delete_log(log_id):
    log = models.Log.query.get(log_id)
    if log is None:
        abort(404)

    flight_id = log.flight_id
    flight = models.Flight.query.get(flight_id = flight_id)
    project = models.Project.query.get(flight.project_id)
    
    
    if current_user.id != project.user_id:
        abort(404)
    else:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], log.filename))
        db.session.delete(log)
        db.session.commit()
        
        return redirect(url_for('view_flight', flight_id=flight_id))

