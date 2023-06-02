from flask import flash, redirect
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE

class Nurse:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.specialty = data['specialty']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get(cls, data):
        query = """SELECT * FROM nurses
                    WHERE id = %(id)s"""
        result = connectToMySQL(DATABASE).query_db(query, data)
        return cls(result[0])
    
    @classmethod
    def get_all(cls):
        query = """SELECT * FROM nurses"""
        result = connectToMySQL(DATABASE).query_db(query)

        all_nurses = []
        for nurse in result:
            all_nurses.append(cls(nurse))
        return all_nurses