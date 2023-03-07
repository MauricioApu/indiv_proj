from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
import re
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['name']
        self.last_name = data['last_name']
        self.alias = data['alias']
        self.age = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @staticmethod
    def validate(user):
        is_valid = True  
        if len(user['name']) < 2:
            flash("Name must be at least 2 characters.")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 1 character.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address.")
            is_valid = False
        if connectToMySQL('indiv_proj').query_db("select * from users where email='"+user['email']+"'"):
            flash("Email address already in use.")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters.")
            is_valid = False
        if user['conpassword'] != user['password']:
            flash("Passwords don't match.")
            is_valid = False

        return is_valid

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users ( name , last_name , email , password, created_at, updated_at) VALUES ( %(name)s , %(last_name)s , %(email)s ,%(password)s, NOW() , NOW() );"
        
        return connectToMySQL('indiv_proj').query_db(query, data)

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("indiv_proj").query_db(query, data)
        
        if len(result) < 1:
            return False
        return cls(result[0])

    # @classmethod
    # def get_by_id(cls, data):
    #     query = "SELECT u.id,u.name, p.content FROM users as u join posts as p WHERE u.id = p.user_id and p.user_id=%(userid)s;"
    #     result = connectToMySQL("indiv_proj").query_db(query, data)
        
    #     if len(result) < 1:
    #         return False
    #     return result
    @classmethod
    def get_by_id(cls, data):
        query = "select u.id, u.alias, u.name, p.content, p.created_at, p.updated_at, p.user_id, count(l.id) as likes from posts as p left join users as u on user_id=u.id left join likes as l on p.id=l.post_id where p.user_id=%(userid)s group by  u.name, p.content, p.id, p.created_at, p.updated_at, p.user_id"
        result = connectToMySQL("indiv_proj").query_db(query, data)
        print(result)
        if len(result) < 1:
            return False
        return result
    
    # @classmethod
    # def get_data(cls, data):
    #     query = "SELECT u.id,u.name, count(l.user_id), count(p.user_id) FROM users as u join posts as p WHERE u.id = p.user_id and p.user_id=%(userid)s;"
    #     result = connectToMySQL("indiv_proj").query_db(query, data)
        
    #     if len(result) < 1:
    #         return False
    #     return result

    @classmethod
    def get_numlikes(cls, data):
        query = "SELECT count(l.id) FROM users as u left join likes as l on l.user_id=u.id where u.id=%(userid)s;"
        result = connectToMySQL("indiv_proj").query_db(query, data)
        
        if len(result) < 1:
            return False
        return result
    
    
    @classmethod
    def get_numposts(cls, data):
        query = "SELECT count(p.id) FROM users as u left join posts as p on u.id = p.user_id  where u.id=%(userid)s;"
        result = connectToMySQL("indiv_proj").query_db(query, data)
        
        if len(result) < 1:
            return False
        return result
    
    @classmethod
    def get_name_lname_email(cls, id):
        query = "SELECT id, alias, name, last_name, email FROM users WHERE id=%(userid)s"
        result = connectToMySQL('indiv_proj').query_db(query, id)
        print(result)
        return result
    
    @classmethod
    def get_name(cls, id):
        query = "SELECT name FROM users WHERE id=%(userid)s"
        data = {
            'userid': id
        }
        result = connectToMySQL('indiv_proj').query_db(query, data)
        return result
    
    @classmethod
    def get_alias(cls, id):
        query = "SELECT alias FROM users WHERE id=%(userid)s"
        data = {
            'userid': id
        }
        result = connectToMySQL('indiv_proj').query_db(query, data)
        return result
 
    