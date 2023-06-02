from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user_symptom_model import UserSymptom
from flask_app.models.user_model import User
from flask_app.models.symptom_model import Symptom

@app.route('/symptom_tracker')
def symptom_tracker_index():
    if 'user_id' not in session:
        return redirect('/users/signin_reg')

    return render_template('symptom_tracker.html',
                            user_symptoms = UserSymptom.get_all({'id':session['user_id']}))

@app.route('/symptom_tracker/add')
def add_user_symptom():
    return render_template('symptom_add.html',
                            logged_user = User.get_user_by_id({'id' : session['user_id']}),
                            all_symptoms = Symptom.get_all())

@app.route('/symptom_tracker/create', methods=["POST"])
def create_user_symptom():
    if not UserSymptom.validate(request.form):
        return redirect('/symptom_tracker/add')
    
    UserSymptom.create(request.form)
    return redirect('/symptom_tracker')

@app.route('/edit/<int:symptom_id>')
def edit(symptom_id):
    symptom = UserSymptom.get_one({ 'id' : symptom_id })
    print(symptom)
    return render_template('symptom_edit.html', 
                            logged_user = User.get_user_by_id({'id' : session['user_id']}),
                            symptom = UserSymptom.get_one({ 'id' : symptom_id }),
                            all_symptoms = Symptom.get_all())

@app.route('/symptom_tracker/edit/process', methods=['POST'])
def process_edit():
    UserSymptom.update(request.form)
    return redirect('/symptom_tracker')

@app.route('/delete/<int:symptom_id>')
def delete(symptom_id):
    UserSymptom.remove({'id' : symptom_id})
    return redirect('/symptom_tracker')
