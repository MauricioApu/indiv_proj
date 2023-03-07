from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app


class Like:
    def __init__(self, data):
        self.id = data['id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.post_id = data['post_id']

    @staticmethod
    def count(data):
        query = "SELECT COUNT(id) FROM likes WHERE post_id=%(post_id)s;"
        return connectToMySQL('indiv_proj').query_db(query, data)

    @classmethod
    def like(cls,data):
        query = "INSERT INTO likes ( created_at, updated_at, user_id, post_id) VALUES ( NOW() , NOW(), %(user_id)s, %(post_id)s );"
        return connectToMySQL('indiv_proj').query_db(query, data)

    @classmethod
    def dislike(cls,data):
        query = "delete from likes where user_id=%(user_id)s and post_id=%(post_id)s limit 1;"
        return connectToMySQL('indiv_proj').query_db(query, data)
