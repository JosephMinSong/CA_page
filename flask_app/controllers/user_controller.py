from flask import render_template, redirect, request, session, flash, jsonify
from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.cancer_model import Cancer
from flask_app.models.doctor_model import Doctor
from flask_app.models.app_model import Advanced_Provider
from flask_app.models.nurse_model import Nurse
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# All renders/redirects
@app.route('/')
def index():
    if 'user_id' in session:
        logged_user = User.get_user_by_id({'id' : session['user_id']})
    else:
        logged_user = False

    return render_template('index.html',
                            logged_user=logged_user)

@app.route('/users/signin_reg')
def sign_in_reg():
    return render_template('signin_reg.html')

@app.route('/users/register/providers')
def register_providers():
    return render_template('register_providers.html',
                            all_cancers = Cancer.get_all(),
                            all_doctors = Doctor.get_all(),
                            all_advanced_providers = Advanced_Provider.get_all(),
                            all_nurses = Nurse.get_all())

@app.route('/diet_guidelines')
def diet_guidelines():
    return render_template('diet_guidelines.html')

@app.route('/users/signout')
def signout():
    session.clear()
    return redirect('/')

@app.route('/reset')
def reset():
    session.clear()
    return redirect('/')


# All Posts
@app.route('/users/register', methods=['POST'])
def register():
    if not User.validate_user_reg(request.form):
        return redirect('/users/signin_reg')
    hashed_pass = bcrypt.generate_password_hash(request.form['password'])

    session['first_name'] = request.form['first_name']
    session['last_name'] = request.form['last_name']
    session['email'] = request.form['email']
    session['password'] = hashed_pass
    return redirect('/users/register/providers')

@app.route('/users/providers/first_form', methods=['POST'])
def first_form():
    all_errors = User.validate_user_provider_reg(request.form)
    return jsonify(all_errors)

@app.route('/users/register/create', methods=['POST'])
def reg_providers():
    user_data = {
        **request.form,
        'first_name' : session['first_name'],
        'last_name' : session['last_name'],
        'email' : session['email'],
        'password' : session['password'],
    }
    new_user = User.create_user(user_data)
    session.clear()
    session['user_id'] = new_user
    return redirect('/')


@app.route('/users/login', methods=['POST'])
def login():
    if not User.validate_user_login(request.form):
        return redirect('/users/signin_reg')
    
    session['user_id'] = User.get_user_by_email(request.form).id
    return redirect('/')

