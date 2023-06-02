from flask import flash, redirect
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app.models import doctor_model
from flask_app.models import app_model
from flask_app.models import nurse_model
from flask_bcrypt import Bcrypt
import re
bcrypt = Bcrypt(app)

email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
password_regex = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,}$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.cancer_id = data['cancer_id']
        self.date_of_dx = data['date_of_dx']
        self.doctor_id = data['doctor_id']
        self.advanced_providers_id = data['advanced_providers_id']
        self.nurse_id = data['nurse_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def create_user(cls, data):
        query = """INSERT INTO users (first_name, last_name, email, password, cancer_id, date_of_dx, doctor_id, advanced_providers_id, nurse_id)
                    VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(cancer_id)s, %(date_of_dx)s, %(doctor_id)s, %(advanced_providers_id)s, %(nurse_id)s);"""

        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_user_by_id(cls, data):
        query = """SELECT * FROM users
                    WHERE id = %(id)s"""
        result = connectToMySQL(DATABASE).query_db(query, data)[0]
        if result:
            doctor_data = {
                'id' : result['doctor_id']
            }
            app_data = {
                'id' : result['advanced_providers_id']
            }
            nurse_data = {
                'id' : result['nurse_id']
            }
            user = cls(result)
            user.doctor = doctor_model.Doctor.get(doctor_data)
            user.app = app_model.Advanced_Provider.get(app_data)
            user.nurse = nurse_model.Nurse.get(nurse_data)

            return user
        return False

    @classmethod
    def get_user_by_email(cls, data):
        query = """SELECT * FROM users
                    WHERE email = %(email)s"""
        result = connectToMySQL(DATABASE).query_db(query, data)
        if result:
            return cls(result[0])
        return False
    
    @classmethod
    def validate_user_login(cls, data):
        query = """SELECT * FROM users
                    WHERE email = %(email)s"""
        result = connectToMySQL(DATABASE).query_db(query, data)
        print(result)
        if result:
            user = cls(result[0])
        else:
            flash("Invalid credentials", 'login')
            return False
        
        if not User.get_user_by_email(data):
            flash("Invalid credentials", 'login')
            return False
        
        if not bcrypt.check_password_hash(user.password, data['password']):
            flash("Invalid credentials", 'login')
            return False
        
        return user
        
    @staticmethod
    def validate_user_provider_reg(data):
        errors = []
        if len(data['date_of_dx']) < 1:
            errors.append('Date must not be empty')
        return errors

    @staticmethod
    def validate_user_reg(data):
        is_valid = True
        # Check first name
        if len(data['first_name']) < 1 :
            flash("Please enter a first name", 'first_name')
            is_valid = False
        elif len(data['first_name']) < 2:
            flash("First name must be at least 2 characters long", 'first_name')
            is_valid = False

        # Check last name
        if len(data['last_name']) < 1 :
            flash("Please enter a last name", 'last_name')
            is_valid = False
        elif len(data['last_name']) < 2:
            flash("Last name must be at least 2 characters long", 'last_name')
            is_valid = False

        # Check email
        if len(data['email']) < 1 :
            flash("Please enter an email address", 'email')
            is_valid = False
        elif not email_regex.match(data['email']):
            flash("Please enter a valid email address", 'email')
            is_valid = False
        else:
            email_data = {'email' : data['email']}
            if User.get_user_by_email(email_data):
                flash("A user already exists with this email", 'email')
                is_valid = False
        
        # Check password
        if len(data['password']) < 1 :
            flash("Please enter a password", 'password')
            is_valid = False
        elif len(data['password']) < 8 :
            flash("Password must be at least 8 characters long", 'password')
            is_valid = False
        elif not password_regex.match(data['password']):
            flash("Password must contain 1 uppercase letter, a number, and a special character", 'password')
            is_valid = False
        
        # Check if passwords match
        if not data['confirm_password']:
            flash("Confirm your password", 'confirm_password')
            is_valid = False
        elif data['password'] != data['confirm_password']:
            flash("Passwords must match", 'confirm_password')
            is_valid = False
        
        return is_valid