from flask import flash, redirect
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app.models import symptom_model

class UserSymptom:
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.symptom_id = data['symptom_id']
        self.severity = data['severity']
        self.date = data['date']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls, data):
        query = """SELECT * FROM user_symptoms
                    JOIN symptoms ON user_symptoms.symptom_id = symptoms.id
                    WHERE user_symptoms.user_id = %(id)s"""
        result = connectToMySQL(DATABASE).query_db(query, data)

        if result:
            all_user_symptoms = []
            for one_symptom in result:
                print(one_symptom)
                user_symptom = cls(one_symptom)
                user_symptom.name = one_symptom['name']
                all_user_symptoms.append(user_symptom)

            return all_user_symptoms
        return False
    
    @classmethod
    def create(cls, data):
        query = """INSERT INTO user_symptoms (user_id, symptom_id, severity, date, description)
                    VALUES (%(user_id)s, %(symptom_id)s, %(severity)s, %(date)s, %(description)s)"""
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def remove(cls, data):
        query = """DELETE FROM user_symptoms
                    WHERE id = %(id)s"""
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def update(cls, data):
        query = """UPDATE user_symptoms
                    SET symptom_id = %(symptom_id)s,
                    user_id = %(user_id)s,
                    severity = %(severity)s,
                    date = %(date)s,
                    description = %(description)s
                    WHERE id = %(id)s
                    """
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def get_one(cls, data):
        query = """SELECT * FROM user_symptoms
                    WHERE id = %(id)s"""
        return connectToMySQL(DATABASE).query_db(query, data)[0]
    
    @staticmethod
    def validate(data):
        is_valid = True
        if len(data['date']) < 1:
            flash('Please enter a date', 'add_symptom')
            is_valid = False
        if len(data['symptom_id']) < 1:
            flash("Please select a symptom", 'add_symptom')
            is_valid = False
        if len(data['severity']) < 1:
            flash('Please select a severity', 'add_symptom')
            is_valid = False
        if len(data['description']) < 1:
            flash("Please enter a description", 'add_symptom')
            is_valid = False
        return is_valid
