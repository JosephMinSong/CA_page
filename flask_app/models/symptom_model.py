from flask import flash, redirect
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE

class Symptom:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create(cls, data):
        query = """INSERT INTO symptoms (name)
                    VALUES (%(name)s)"""
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def get_all(cls):
        query = """SELECT * FROM symptoms"""
        result = connectToMySQL(DATABASE).query_db(query)

        all_symptoms = []
        for symptom in result:
            all_symptoms.append(cls(symptom))
        return all_symptoms
    
    