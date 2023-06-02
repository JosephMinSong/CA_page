from flask import flash, redirect
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE

class Cancer:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def get_all(cls):
        query = """SELECT * FROM cancers"""
        result = connectToMySQL(DATABASE).query_db(query)

        all_cancers = []
        for cancer in result:
            all_cancers.append(cls(cancer))
        return all_cancers
    
    