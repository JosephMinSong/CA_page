from flask import flash, redirect
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE

class Doctor:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.title = data['title']
        self.specialty = data['specialty']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get(cls, data):
        query = """SELECT * FROM doctors
                    WHERE id = %(id)s"""
        result = connectToMySQL(DATABASE).query_db(query, data)
        return cls(result[0])
    
    @classmethod
    def get_all(cls):
        query = """SELECT * FROM doctors"""
        result = connectToMySQL(DATABASE).query_db(query)

        all_doctors = []
        for doctor in result:
            all_doctors.append(cls(doctor))
        return all_doctors
    

